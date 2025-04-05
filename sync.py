import csv
import subprocess
from bisect import bisect_left


def read_gcsv_file(gcsv_file):
    times = []
    rx_vals, ry_vals, rz_vals = [], [], []
    ax_vals, ay_vals, az_vals = [], [], []
    time_offset = 0.0  # Offset acumulativo de tiempo

    with open(gcsv_file, newline="") as f:
        reader = csv.reader(f)
        tscale = gscale = ascale = None
        header_passed = False
        for row in reader:
            if not header_passed:
                if len(row) > 0 and row[0] == "t":
                    header_passed = True
                else:
                    if len(row) >= 2:
                        if row[0] == "tscale":
                            tscale = float(row[1])
                        if row[0] == "gscale":
                            gscale = float(row[1])
                        if row[0] == "ascale":
                            ascale = float(row[1])
                continue

            if len(row) >= 7:
                t_raw = float(row[0])
                rx_raw = float(row[1])
                ry_raw = float(row[2])
                rz_raw = float(row[3])
                ax_raw = float(row[4])
                ay_raw = float(row[5])
                az_raw = float(row[6])

                timestamp = time_offset + t_raw * tscale
                rx = rx_raw * gscale
                ry = ry_raw * gscale
                rz = rz_raw * gscale
                ax = ax_raw * ascale
                ay = ay_raw * ascale
                az = az_raw * ascale

                times.append(timestamp)
                rx_vals.append(rx)
                ry_vals.append(ry)
                rz_vals.append(rz)
                ax_vals.append(ax)
                ay_vals.append(ay)
                az_vals.append(az)

    return times, rx_vals, ry_vals, rz_vals, ax_vals, ay_vals, az_vals


def get_total_frames(video_file):
    ffprobe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-count_frames",
        "-show_entries",
        "stream=nb_read_frames",
        "-of",
        "csv=p=0",
        video_file,
    ]
    result = subprocess.run(
        ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode == 0:
        return int(result.stdout.strip())
    else:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")


def synchronize_data(
    times, rx_vals, ry_vals, rz_vals, ax_vals, ay_vals, az_vals, total_frames, fps=60
):
    frame_times = [n / fps for n in range(total_frames)]
    sensor_index = 0
    synced_data = []

    for frame_num, t_frame in enumerate(frame_times):
        idx = bisect_left(times, t_frame, lo=sensor_index)

        if idx == 0:
            closest_idx = 0
        elif idx >= len(times):
            closest_idx = len(times) - 1
        else:
            prev_idx = idx - 1
            next_idx = idx
            if abs(times[prev_idx] - t_frame) <= abs(times[next_idx] - t_frame):
                closest_idx = prev_idx
            else:
                closest_idx = next_idx

        timestamp = times[closest_idx]
        rx_val = rx_vals[closest_idx]
        ry_val = ry_vals[closest_idx]
        rz_val = rz_vals[closest_idx]
        ax_val = ax_vals[closest_idx]
        ay_val = ay_vals[closest_idx]
        az_val = az_vals[closest_idx]

        synced_data.append(
            [frame_num, timestamp, rx_val, ry_val, rz_val, ax_val, ay_val, az_val]
        )
        sensor_index = max(0, closest_idx - 1)

    return synced_data


def save_to_csv(synced_data, output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "timestamp", "rx", "ry", "rz", "ax", "ay", "az"])
        for row in synced_data:
            writer.writerow(row)


gcsv_file = "Runcam6_0002.gcsv"
video_file = "Runcam6_0002.MP4"
total_frames = get_total_frames(video_file)

# Leer archivo GCSV
(times, rx_vals, ry_vals, rz_vals, ax_vals, ay_vals, az_vals) = read_gcsv_file(
    gcsv_file
)

# Sincronizar datos
synced_data = synchronize_data(
    times, rx_vals, ry_vals, rz_vals, ax_vals, ay_vals, az_vals, total_frames
)

# Guardar en CSV
save_to_csv(synced_data, "video_sensor_sync.csv")

print("Proceso completado. Archivo CSV generado correctamente.")
