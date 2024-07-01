import PySimpleGUI as sg
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

# Definir el diseño de la interfaz gráfica
sg.theme('DarkBlue14')  # Cambiar tema para mejorar la estética

layout = [
    [sg.Image(filename="D:/programas/logo.png", size=(230, 230))],  # Asegúrate de que esta ruta sea correcta
    [sg.Text("Introduce la URL del video de YouTube:", font=('Helvetica', 12))],
    [sg.InputText(key='-URL-', size=(50, 1))],
    [sg.Text("Selecciona la carpeta de destino:", font=('Helvetica', 12))],
    [sg.InputText(default_text="C:/Users/david/Music", key='-FOLDER-', size=(38, 1)), sg.FolderBrowse('Examinar')],
    [sg.Button('Descargar', size=(10, 1))],
    [sg.ProgressBar(max_value=100, orientation='h', size=(25, 5), key='-PROGRESS-', bar_color=('red', 'white'))],
    [sg.Text('', key='-PERCENTAGE-', size=(5, 1), font=('Helvetica', 10))],
    [sg.Text('', size=(60, 1), key='-STATUS-', font=('Helvetica', 10))],
    [sg.Text('', size=(60, 1), key='-TITLE-', font=('Helvetica', 10))],
    [sg.Text('', size=(60, 1), key='-AUTHOR-', font=('Helvetica', 10))],
    [sg.Text('', size=(60, 1), key='-DURATION-', font=('Helvetica', 10))],
    [sg.Button('Salir', size=(5, 1), button_color=('white', 'red'), font=('Helvetica', 10))]
]

# Crear la ventana
window = sg.Window('Descargador de Audio de YouTube', layout, element_justification='center', finalize=True)

# Bucle de eventos
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Salir':
        break
    if event == 'Descargar':
        window['-PERCENTAGE-'].update('0%')
        window['-PROGRESS-'].update_bar(0)
        
        url = values['-URL-']
        folder = values['-FOLDER-']
        status, title, author, duration, elapsed_time = download_audio_from_youtube(url, folder, window)
        window['-STATUS-'].update(status)
        if title and author and duration:
            window['-TITLE-'].update(f"Titulo: {title}")
            window['-AUTHOR-'].update(f"Autor: {author}")
            window['-DURATION-'].update(f"Duración: {duration}")

# Cerrar la ventana
window.close()
