#!/bin/bash

# --------------------------------------
# Bash script to run gyroflow stabilization on a video
# --------------------------------------

# TODO get from config file
VIDEO_DIR="videos"
GCSV_DIR="gcsv"
PRESET_PATH="./presets/9C33-6BBD_presets.json"  # TODO get from config file

# Función de ayuda
usage() {
    echo "Uso: $0 -v VIDEO_FILENAME -g GCSV_FILENAME"
    exit 1
}

# Parseo de argumentos
while getopts ":v:g:" opt; do
  case ${opt} in
    v )
      VIDEO_FILENAME=$OPTARG
      ;;
    g )
      GCSV_FILENAME=$OPTARG
      ;;
    \? )
      usage
      ;;
  esac
done

# Comprobamos que se hayan pasado los argumentos requeridos
if [ -z "$VIDEO_FILENAME" ] || [ -z "$GCSV_FILENAME" ]; then
    usage
fi

# Directorio base (el del script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Construimos las rutas completas
VIDEO_PATH="${SCRIPT_DIR}/${VIDEO_DIR}/${VIDEO_FILENAME}"
GCSV_PATH="${SCRIPT_DIR}/${GCSV_DIR}/${GCSV_FILENAME}"

# Mostrar el directorio actual
pwd

# Construir y ejecutar el comando
CMD="./Gyroflow/gyroflow \"$VIDEO_PATH\" -g \"$GCSV_PATH\" --preset \"$PRESET_PATH\" -f"
echo "Ejecutando: $CMD"
eval $CMD
