import PySimpleGUI as sg
from funciones import download_audio_from_youtube

# Definir el diseño de la interfaz gráfica
sg.theme('DarkBlue14')  # Cambiar tema para mejorar la estética

layout = [
    #[sg.Image(filename="RUTA_ABSOLUTA/recursos/logo.png", size=(230, 230))],  # Existe logo.png y logo2.png
    [sg.Text("Introduce la URL del video de YouTube:", font=('Helvetica', 12))],
    [sg.InputText(key='-URL-', size=(50, 1))],
    [sg.Text("Selecciona la carpeta de destino:", font=('Helvetica', 12))],
    [sg.InputText(default_text="", key='-FOLDER-', size=(38, 1)), sg.FolderBrowse('Examinar')],
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
