import csv
import cv2
import numpy as np
import sys

def read_csv_data(csv_file):
    synced_data = []
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)  # Leer encabezado
        for row in reader:
            frame_num = int(row[0])
            timestamp = float(row[1])
            rx = float(row[2])
            ry = float(row[3])
            rz = float(row[4])
            ax = float(row[5])
            ay = float(row[6])
            az = float(row[7])
            synced_data.append([frame_num, timestamp, rx, ry, rz, ax, ay, az])
    return synced_data

def overlay_video_with_data(video_file, csv_file, output_file="output_with_overlay.mp4", fps=60):
    synced_data = read_csv_data(csv_file)

    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx >= len(synced_data):
            break

        # Obtener datos sincronizados para este frame
        data = synced_data[frame_idx]
        _, timestamp, rx, ry, rz, ax, ay, az = data

        # Dibujar overlay en el frame
        text = f"Timestamp: {timestamp:.3f} s | Rx: {rx:.3f} | Ry: {ry:.3f} | Rz: {rz:.3f} | Ax: {ax:.3f} | Ay: {ay:.3f} | Az: {az:.3f}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 superponer_overlay.py <archivo_video.mp4> <archivo_csv.csv>")
        sys.exit(1)

    video_file = sys.argv[1]
    csv_file = sys.argv[2]

    overlay_video_with_data(video_file, csv_file)

    print("Proceso completado. Video con overlay generado correctamente.")
