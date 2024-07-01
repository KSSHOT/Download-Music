from pytube import YouTube
from pydub import AudioSegment
import os
import time

def download_audio_from_youtube(url, output_path, window):
    try:
        start_time = time.time()
        
        # Crear el directorio de salida si no existe
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Descargar el video de YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        window['-PERCENTAGE-'].update('25%')
        window['-PROGRESS-'].update_bar(25)
        out_file = video.download(output_path=output_path)

        # Actualizar el progreso al 50% (aproximadamente para la descarga)
        window['-PERCENTAGE-'].update('50%')
        window['-PROGRESS-'].update_bar(50)

        # Muestra información básica del video
        title = yt.title
        author = yt.author
        duration_seconds = int(yt.length)
        minutes, seconds = divmod(duration_seconds, 60)
        duration = f"{minutes}:{seconds:02d}"

        # Convertir el archivo descargado a mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        audio = AudioSegment.from_file(out_file)
        window['-PERCENTAGE-'].update('75%')
        window['-PROGRESS-'].update_bar(75)
        audio.export(new_file, format="mp3")

        # Eliminar el archivo original
        os.remove(out_file)

        # Actualizar el progreso al 100% (finalización de la conversión)
        window['-PROGRESS-'].update_bar(100)
        window['-PERCENTAGE-'].update('100%')

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        elapsed_time_formatted = f"{int(minutes)}:{int(seconds):02d}"

        return (f"Ruta: {new_file}", title, author, duration, elapsed_time_formatted)
    except Exception as e:
        return (f'Ocurrió un error: {e}', None, None, None, None)
