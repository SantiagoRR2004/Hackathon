import pandas as pd
from ultralytics import YOLO
import cv2
from tqdm import tqdm

# Función para cargar y analizar el CSV
def cargar_csv(path):
    """
    Loads the CSV file containing synchronized data.
    """
    return pd.read_csv(path) #, header=0, names=['frame', 'timestamp', 'rx', 'ry', 'rz', 'ax', 'ay', 'az'])

# Calcular umbrales estadísticos para frenazos
def calcular_umbrales(data, desviaciones=3):
    """
    Calculates statistical thresholds for detecting sudden stops (frenazos).
    """
    stats = data[['ax', 'ay', 'az']].describe() # Axis statistics
    thresholds = {eje: stats[eje]['mean'] - desviaciones * stats[eje]['std'] for eje in ['ax', 'ay', 'az']}
    # Calculate thresholds based on mean and std deviation
    return thresholds

# Detectar frenazos a partir de umbrales
def detectar_frenazos(data, thresholds):
    """
    Detects sudden stops (frenazos) based on the calculated thresholds.
    """
    data['frenazo'] = (
        (data['ax'] < thresholds['ax']) |
        (data['ay'] < thresholds['ay']) |
        (data['az'] < thresholds['az'])
    ) # Detect sudden stops based on thresholds
    return data[data['frenazo']]

# Segmentar video y contar frenazos en cada segmento
def segmentar_video(data, frenazos, segment_duration=5):
    """
    Segments the video into intervals and counts the number of frenazos in each segment.
    """
    total_time = data['timestamp'].max() # Get the maximum timestamp
    segments = [(start, min(start + segment_duration, total_time)) for start in range(0, int(total_time) + 1, segment_duration)]
    # Create segments of the video based on the segment duration

    segment_data = [] # Initialize list to store segment data
    for start, end in segments: # Create segments of the video
        frenazos_in_segment = frenazos[(frenazos['timestamp'] >= start) & (frenazos['timestamp'] < end)]
        # Count the number of frenazos in the current segment

        # Calculate the average number of cars and persons per frame
        segment_data.append({
            'start': start,
            'end': end,
            'duration': end - start,
            'frenazo_count': len(frenazos_in_segment),
            'car_count_per_frame': [],
            'person_count_per_frame': [],
            'score': 0
        })

    return pd.DataFrame(segment_data)

# Detectar objetos usando YOLO

def detectar_objetos_yolo(video_path, segments_df, confidence=0.3):
    """
    Detects objects in the video using YOLO and counts the number of cars and persons.
    """
    model = YOLO('yolov8n.pt') # Load YOLO model
    cap = cv2.VideoCapture(video_path) # Open video file
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # Get total number of frames

    for _ in tqdm(range(total_frames), desc="Procesando YOLO", unit="frame"): # Read each frame
        ret, frame = cap.read() # Read frame from video
        if not ret: # If frame not read, break the loop
            break

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 # Get current timestamp
        segmento_actual = segments_df[(segments_df['start'] <= timestamp) & (segments_df['end'] > timestamp)]

        if segmento_actual.empty:
            continue

        results = model(frame, verbose=False, conf=confidence)[0]
        car_count = 0
        person_count = 0

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if label == 'car':
                car_count += 1
            elif label == 'person':
                person_count += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        idx = segmento_actual.index[0]
        segments_df.at[idx, 'car_count_per_frame'].append(car_count)
        segments_df.at[idx, 'person_count_per_frame'].append(person_count)

    cap.release()
    return segments_df

# Calcular la puntuación final de cada segmento

def calcular_puntuacion(segments_df, pesos={'frenazo': 2, 'car': 1, 'person': 1.5}):
    """
    Calculates the final score for each segment based on the number of frenazos, cars, and persons detected.
    """
    for index, row in segments_df.iterrows():
        avg_car_count = sum(row['car_count_per_frame']) / len(row['car_count_per_frame']) if row['car_count_per_frame'] else 0
        avg_person_count = sum(row['person_count_per_frame']) / len(row['person_count_per_frame']) if row['person_count_per_frame'] else 0

        segments_df.at[index, 'car_count'] = avg_car_count
        segments_df.at[index, 'person_count'] = avg_person_count

        segments_df.at[index, 'score'] = (
            row['frenazo_count'] * pesos['frenazo'] +
            avg_car_count * pesos['car'] +
            avg_person_count * pesos['person']
        )
    return segments_df


# Generar el video final con Overlay
def generar_video_resumido(video_path, segments_df, output_path='video_resumido_top3.mp4', top_n=3):
    """
    Generates a summarized video composed of the top N segments of 5 seconds each.
    """
    # Seleccionar los 3 mejores segmentos
    top_segments = segments_df.sort_values(by='score', ascending=False).head(top_n)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for _, segmento in top_segments.iterrows():
        start_frame = int(segmento['start'] * fps)
        end_frame = int(segmento['end'] * fps)

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        for _ in range(start_frame, end_frame):
            ret, frame = cap.read()
            if not ret:
                break

            text_overlay = (
                f'Score: {segmento["score"]:.1f}\n'
                f'Frenazos: {segmento["frenazo_count"]}\n'
                f'Coches promedio por frame: {segmento["car_count"]:.1f}\n'
                f'Personas promedio por frame: {segmento["person_count"]:.1f}'
            )

            y0, dy = 30, 30
            for i, line in enumerate(text_overlay.split('\n')):
                y = y0 + i * dy
                cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

            out.write(frame)

    cap.release()
    out.release()



if __name__ == '__main__':
    csv_path = 'video_sensor_sync.csv'
    video_path = 'Runcam6_0002.MP4'
    data = cargar_csv(csv_path)
    thresholds = calcular_umbrales(data)
    frenazos = detectar_frenazos(data, thresholds)
    segments_df = segmentar_video(data, frenazos)
    segments_df = detectar_objetos_yolo(video_path, segments_df)
    segments_df = calcular_puntuacion(segments_df)
    generar_video_resumido(video_path, segments_df, output_path='video_resumido_top3.mp4', top_n=3)
