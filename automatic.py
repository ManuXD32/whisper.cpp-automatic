import os
import subprocess

# Función para extraer el audio de un archivo de vídeo
def extraer_audio(video_path, output_dir):
    video_name = os.path.basename(video_path)
    audio_name = os.path.splitext(video_name)[0] + '.wav'
    audio_path = os.path.join(output_dir, audio_name)
    
    ffmpeg_cmd = f'ffmpeg -i "{video_path}" -hide_banner -vn -loglevel error -ar 16000 -ac 1 -c:a pcm_s16le -y "{audio_path}"'
    subprocess.call(ffmpeg_cmd, shell=True)
    
    return audio_path

# Función para transcribir el audio usando el modelo de lenguaje
def transcribir_audio(audio_path, output_file, model_path, option):
    transcribe_cmd = f'./main -l auto --output-file "{output_file}" {option} -m "{model_path}" "{audio_path}" -t 12'
    subprocess.call(transcribe_cmd, shell=True)

# Directorio donde se encuentran los vídeos
video_directory = input("Introduce el directorio donde están los vídeos: ")

# Opción de salida para el archivo de texto
output_option = input("¿Deseas usar una opción diferente a -otxt? (dejar en blanco para usar -otxt): ")
if not output_option:
    output_option = '-otxt'

# Directorio de salida para los archivos de audio
output_directory = os.path.join(video_directory, 'output')

# Verificar si la carpeta de salida existe y agregar un número al final si es necesario
i = 1
while os.path.exists(output_directory):
    output_directory = os.path.join(video_directory, f'output-{i}')
    i += 1

os.makedirs(output_directory)

# Directorio donde se encuentran los modelos de lenguaje
model_directory = 'models'

# Obtener lista de archivos .bin en el directorio de modelos
model_files = [f for f in os.listdir(model_directory) if os.path.isfile(os.path.join(model_directory, f)) and f.endswith('.bin')]

# Mostrar lista de modelos disponibles y permitir al usuario elegir uno
print("Modelos disponibles:")
for i, model_file in enumerate(model_files):
    print(f"{i+1}. {model_file}")
model_choice = int(input("Elige el número correspondiente al modelo que deseas utilizar: "))
model_path = os.path.join(model_directory, model_files[model_choice-1])

# Obtener lista de archivos de vídeo en el directorio
video_files = [f for f in os.listdir(video_directory) if os.path.isfile(os.path.join(video_directory, f))]

# Procesar cada archivo de vídeo
for video_file in video_files:
    video_path = os.path.join(video_directory, video_file)
    
    # Extraer el audio del vídeo
    audio_path = extraer_audio(video_path, output_directory)
    
    # Transcribir el audio y guardar el resultado
    output_file = os.path.splitext(video_file)[0] + '.txt'
    
    # Verificar si el archivo de salida ya existe en la carpeta "output" y agregar un número al final si es necesario
    i = 1
    while os.path.exists(os.path.join(output_directory, output_file)):
        name, ext = os.path.splitext(output_file)
        output_file = f"{name}-{i}{ext}"
        i += 1
    
    output_path = os.path.join(output_directory, output_file)
    transcribir_audio(audio_path, output_path, model_path, output_option)
