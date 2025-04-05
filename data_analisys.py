import pandas as pd
from ultralytics import YOLO
import cv2
from tqdm import tqdm

# Función para cargar y analizar el CSV
def cargar_csv(path):
    return pd.read_csv(path)

# Calcular umbrales estadísticos para frenazos
def calcular_umbrales(data, desviaciones=3):
    stats = data[['ax', 'ay', 'az']].describe()
    thresholds = {eje: stats[eje]['mean'] - desviaciones * stats[eje]['std'] for eje in ['ax', 'ay', 'az']}
    return thresholds

# Detectar frenazos a partir de umbrales
def detectar_frenazos(data, thresholds):
    data['frenazo'] = (
        (data['ax'] < thresholds['ax']) |
        (data['ay'] < thresholds['ay']) |
        (data['az'] < thresholds['az'])
    )
    return data[data['frenazo']]

# Segmentar video y contar frenazos en cada segmento
def segmentar_video(data, frenazos, segment_duration=5):
    total_time = data['timestamp'].max()
    segments = [(start, min(start + segment_duration, total_time)) for start in range(0, int(total_time) + 1, segment_duration)]

    segment_data = []
    for start, end in segments:
        frenazos_in_segment = frenazos[(frenazos['timestamp'] >= start) & (frenazos['timestamp'] < end)]

        segment_data.append({
            'start': start,
            'end': end,
            'duration': end - start,
            'frenazo_count': len(frenazos_in_segment),
            'car_count': 0,
            'person_count': 0,
            'score': 0
        })

    return pd.DataFrame(segment_data)

# Detectar objetos usando YOLO

def detectar_objetos_yolo(video_path, segments_df, confidence=0.3):
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for _ in tqdm(range(total_frames), desc="Procesando YOLO", unit="frame"):
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        segmento_actual = segments_df[(segments_df['start'] <= timestamp) & (segments_df['end'] > timestamp)]

        if segmento_actual.empty:
            continue

        results = model(frame, verbose=False, conf=confidence)[0]
        car_count = sum(1 for cls in results.boxes.cls if model.names[int(cls)] == 'car')
        person_count = sum(1 for cls in results.boxes.cls if model.names[int(cls)] == 'person')

        idx = segmento_actual.index[0]
        segments_df.at[idx, 'car_count'] += car_count
        segments_df.at[idx, 'person_count'] += person_count

    cap.release()
    return segments_df

# Calcular la puntuación final de cada segmento
def calcular_puntuacion(segments_df, pesos={'frenazo': 2, 'car': 1, 'person': 1.5}):
    segments_df['score'] = (
        segments_df['frenazo_count'] * pesos['frenazo'] +
        segments_df['car_count'] * pesos['car'] +
        segments_df['person_count'] * pesos['person']
    )
    return segments_df

# Generar el video final con OpenCV
def generar_video_resumido(video_path, segments_df, output_path='video_resumido.mp4'):
    top_segments = segments_df.sort_values(by='score', ascending=False).head(3)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for _, segment in tqdm(top_segments.iterrows(), desc="Generando video", total=3, unit="segmento"):
        cap.set(cv2.CAP_PROP_POS_MSEC, segment['start'] * 1000)

        while cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 <= segment['end']:
            ret, frame = cap.read()
            if not ret:
                break

            text = f'Score: {segment['score']:.1f}\nFrenazos: {segment['frenazo_count']}\nCoches: {segment['car_count']}\nPersonas: {segment['person_count']}'
            y0, dy = 30, 30
            for i, line in enumerate(text.split('\n')):
                y = y0 + i * dy
                cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            out.write(frame)

    cap.release()
    out.release()


def main(csv_path, video_path):
    data = cargar_csv(csv_path)
    thresholds = calcular_umbrales(data)
    frenazos = detectar_frenazos(data, thresholds)
    segments_df = segmentar_video(data, frenazos)
    segments_df = detectar_objetos_yolo(video_path, segments_df)
    segments_df = calcular_puntuacion(segments_df)

    generar_video_resumido(video_path, segments_df)


if __name__ == '__main__':
    csv_path = 'video_sensor_sync.csv'
    video_path = 'Runcam6_0002.MP4'
    main(csv_path, video_path)
