import os
from tkinter import *
import threading
import time
from pytube import YouTube
from ttkthemes import ThemedTk
from tkinter import Button, Frame, Label, Entry, StringVar, Radiobutton
from tkinter import filedialog, font, ttk

def exit_application():
    main.destroy()

def update_message_label(message):
    MENSAJE.config(text=message)

def download_audio(link, audio_path):
    try:
        calidad = calidad_audio_var.get()

        if link:
            yt = YouTube(link)
            audio_file_path = os.path.join(audio_path, f"{yt.title}_{calidad}.mp3")

            os.chdir(audio_path)

            stream = yt.streams.filter(only_audio=True, abr=calidad).first()

            if stream:
                stream.download(filename="temp_audio")
                os.rename("temp_audio", audio_file_path)
                update_message_label(f"Audio descargado con éxito: {audio_file_path}")
            else:
                raise ValueError(f"No se encontró una corriente de audio con calidad {calidad}")
        else:
            raise ValueError("No existe link")
    except Exception as e:
        update_message_label(f"Error al descargar audio: {str(e)}")
        estado.set("¡ERROR!")
    finally:
        os.chdir(script_directory)
        estado.set("¡DESCARGA COMPLETA!")
        LINK.config(state=NORMAL)
        AUDIO_DOWNLOAD.config(state=NORMAL)
        LINK.delete(0, "end")

def download_video(link, video_path):
    try:
        if link:
            yt = YouTube(link)
            calidad = calidad_video_var.get()
            video_file_path = os.path.join(video_path, f"{yt.title}_{calidad}.mp4")

            os.chdir(video_path)

            stream = yt.streams.filter(res=calidad, progressive=True).first()

            if stream:
                stream.download(filename="temp_video")
                os.rename("temp_video", video_file_path)
                update_message_label(f"Video descargado con éxito: {video_file_path}")
            else:
                raise ValueError(f"No se encontró una corriente de video con calidad {calidad}")
        else:
            raise ValueError("No existe link")
    except Exception as e:
        update_message_label(f"Error al descargar video: {str(e)}")
        estado.set("¡ ERROR !")
    finally:
        os.chdir(script_directory)
        estado.set("¡ DESCARGA COMPLETA !")
        LINK.config(state=NORMAL)
        DOWNLOAD.config(state=NORMAL)
        LINK.delete(0, "end")

def update_progress_bar(block_count, block_size, total_size):
    percent = (block_count * block_size / total_size) * 100
    PROGRESS_BAR['value'] = percent

    now = time.time()
    elapsed_time = now - PROGRESS_BAR.start_time
    PROGRESS_BAR.start_time = now
    speed = (block_size / 1024) / elapsed_time if elapsed_time > 0 else 0

    update_message_label(f"Descargando... {percent:.2f}% - Velocidad: {speed:.2f} KB/s")

def show_downloading_message():
    LINK.config(state=DISABLED)
    AUDIO_DOWNLOAD.config(state=DISABLED)
    DOWNLOAD.config(state=DISABLED)
    PROGRESS_BAR['value'] = 0
    PROGRESS_BAR.start_time = time.time()
    sms = "Descargando"
    pivot = True
    while not estado.get():
        if pivot:
            sms += "."
            if len(sms) == 17:
                pivot = False
        else:
            sms = sms[:-2]
            if len(sms) == 11:
                pivot = True
        update_message_label(sms)
        time.sleep(1/2)

def select_download_directory():
    global AUDIO_PATH, VIDEO_PATH
    selected_directory = filedialog.askdirectory()

    AUDIO_PATH = os.path.abspath(os.path.join(selected_directory, "Descargas", "Audio"))
    VIDEO_PATH = os.path.abspath(os.path.join(selected_directory, "Descargas", "Video"))

    try:
        os.chdir(selected_directory)
        print("Directorio actual después de cambiarlo:", os.getcwd())
    except Exception as e:
        print(f"Error al cambiar al directorio seleccionado: {str(e)}")
        return

    os.makedirs(AUDIO_PATH, exist_ok=True)
    os.makedirs(VIDEO_PATH, exist_ok=True)

    update_message_label(f"Directorio de descarga actualizado: {selected_directory}")

script_directory = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(script_directory, "Descargas", "Audio")
VIDEO_PATH = os.path.join(script_directory, "Descargas", "Video")
os.makedirs(AUDIO_PATH, exist_ok=True)
os.makedirs(VIDEO_PATH, exist_ok=True)

def borrar_contenido_video():
    LINK_VIDEO.delete(0, 'end')

def borrar_contenido_audio():
    LINK.delete(0, 'end')

def cambiar_borde_blanco(event):
    event.widget.config(highlightcolor="white")
    event.widget.config(highlightbackground="white")

def cambiar_borde_rojo(event):
    event.widget.config(highlightcolor="#e74c3c")
    event.widget.config(highlightbackground="#e74c3c")


# Configuración principal
main = ThemedTk(theme="radiance")
main.title("DownloadMaster 1.0")  # Cambia "Mi Aplicación" al título que desees
main.iconbitmap('C:\\Users\\sam10\\Downloads\\DownloadMaster-main\\Icon\\download_icon-icons.com_66472.ico')  # Asegúrate de reemplazar la ruta con la ruta a tu archivo de icono
main.config(bg="#2c3e50")
main.wm_state('zoomed')

# Obtener dimensiones de la pantalla
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

# Dimensiones de la ventana principal
window_width = 800
window_height = 600

# Calcular las coordenadas x, y para centrar la ventana en la pantalla
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Establecer las dimensiones y la posición de la ventana principal
main.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Frame principal
FRAME_MAIN = Frame(main, bg="#2c3e50", width=window_width, height=window_height)
FRAME_MAIN.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Utilizamos sticky para centrar en ambas direcciones

main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)

# Etiqueta de mensaje
MENSAJE = Label(FRAME_MAIN, bg="#2c3e50", fg="white", font=("arial", 12, "bold"))
MENSAJE.grid(row=1, column=0)

estado = StringVar()

Frame(FRAME_MAIN, height=50, bg="#2c3e50").grid(row=2, column=0)

Label(FRAME_MAIN, text="➤ DOWNLOADMASTER", fg="white", bg="#dbad6a", height=2, width=20, font=("Arial", 12, "bold")).grid(row=3, column=0, ipadx=10, ipady=10)

Label(FRAME_MAIN, text="PEGA EL LINK (AUDIO):", bg="#2c3e50", fg="white").grid(row=4, column=0, pady=(20, 0))

# Para el cuadro de audio
audio_frame = Frame(FRAME_MAIN, bg="#2c3e50")
audio_frame.grid(row=5, column=0, ipady=5, pady=(0, 10))

LINK = Entry(audio_frame, width=50, relief=SOLID, highlightthickness=2, highlightcolor="white")
LINK.pack(side=LEFT)
LINK.focus_set()
LINK.bind("<FocusIn>", cambiar_borde_rojo)
LINK.bind("<FocusOut>", cambiar_borde_blanco)

borrar_contenido_button_audio = Button(audio_frame, text="X", bg="red", fg="white", command=borrar_contenido_audio)
borrar_contenido_button_audio.pack(side=LEFT, padx=(10, 0))

calidad_audio_var = StringVar()
calidad_audio_var.set("160kbps")

calidad_audio_frame = Frame(FRAME_MAIN, bg="#2c3e50")
calidad_audio_frame.grid(row=6, column=0, pady=(10, 0))

Label(calidad_audio_frame, text="Calidad de Audio:", bg="#2c3e50", fg="white").pack(side=LEFT)

calidades_audio = ["320kbps", "256kbps", "160kbps",]
for calidad in calidades_audio:
    Radiobutton(calidad_audio_frame, text=calidad, variable=calidad_audio_var, value=calidad, bg="#2c3e50", fg="white").pack(side=LEFT)

AUDIO_DOWNLOAD = Button(FRAME_MAIN, text="DESCARGAR AUDIO", fg="white", bg="#e74c3c", cursor="hand2", command=lambda: threading.Thread(target=download_audio, args=(LINK.get(), AUDIO_PATH)).start())
AUDIO_DOWNLOAD.grid(row=7, column=0, pady=(10, 0))

Frame(FRAME_MAIN, height=50, bg="#2c3e50").grid(row=8, column=0)

Label(FRAME_MAIN, text="➤ DOWNLOADMASTER", fg="white", bg="#dbad6a", height=2, width=20, font=("Arial", 12, "bold")).grid(row=9, column=0, ipadx=10, ipady=10)
Label(FRAME_MAIN, text="PEGA EL LINK (VIDEO):", bg="#2c3e50", fg="white").grid(row=10, column=0, pady=(20, 0))

# Para el cuadro de video
video_frame = Frame(FRAME_MAIN, bg="#2c3e50")
video_frame.grid(row=11, column=0, ipady=5)

LINK_VIDEO = Entry(video_frame, width=50, relief=SOLID, highlightthickness=2, highlightcolor="white")
LINK_VIDEO.pack(side=LEFT)
LINK_VIDEO.focus_set()
LINK_VIDEO.bind("<FocusIn>", cambiar_borde_rojo)
LINK_VIDEO.bind("<FocusOut>", cambiar_borde_blanco)

borrar_contenido_button_video = Button(video_frame, text="X", bg="red", fg="white", command=borrar_contenido_video)
borrar_contenido_button_video.pack(side=LEFT, padx=(10, 0))  # Utiliza sticky="e" para alinear a la derecha

calidad_video_var = StringVar()
calidad_video_var.set("720p")

calidad_video_frame = Frame(FRAME_MAIN, bg="#2c3e50")
calidad_video_frame.grid(row=12, column=0, pady=(10, 0))

Label(calidad_video_frame, text="Calidad de Video:", bg="#2c3e50", fg="white").pack(side=LEFT)

calidades_video = ["1080p", "720p", "480p", "360p"]
for calidad in calidades_video:
    Radiobutton(calidad_video_frame, text=calidad, variable=calidad_video_var, value=calidad, bg="#2c3e50", fg="white").pack(side=LEFT)

DOWNLOAD = Button(FRAME_MAIN, text="DESCARGAR VIDEO", fg="white", bg="#e74c3c", cursor="hand2", command=lambda: threading.Thread(target=download_video, args=(LINK_VIDEO.get(), VIDEO_PATH)).start())
DOWNLOAD.grid(row=13, column=0, padx=10, pady=(20, 0))

Frame(FRAME_MAIN, height=10, bg="#2c3e50").grid(row=14, column=0)

PROGRESS_BAR = ttk.Progressbar(FRAME_MAIN, length=500, mode="determinate")
PROGRESS_BAR.grid(row=15, column=0, pady=(10, 20))
PROGRESS_BAR.start_time = time.time()

Frame(FRAME_MAIN, height=10, bg="#2c3e50").grid(row=16, column=0)

# Frame para los botones
buttons_frame = Frame(FRAME_MAIN, bg="#2c3e50")
buttons_frame.grid(row=17, column=0, pady=(10, 0))

# Botón OPEN_DIR_VIDEO
OPEN_DIR_VIDEO = Button(buttons_frame, text="📂", fg="white", bg="#e74c3c", cursor="hand2", command=lambda: os.startfile(VIDEO_PATH))
OPEN_DIR_VIDEO.pack(side=LEFT)

# Botón CHOOSE_DIR
CHOOSE_DIR = Button(buttons_frame, text="ELEGIR RUTA DE DESCARGA", fg="white", bg="#dbad6a", cursor="hand2", command=select_download_directory)
CHOOSE_DIR.pack(side=LEFT, padx=(10, 0))

# Centrar el Frame en ambas direcciones
FRAME_MAIN.grid_rowconfigure(0, weight=1)
FRAME_MAIN.grid_columnconfigure(0, weight=1)

# Botón de salida en la esquina inferior derecha
exit_button = Button(main, text="Salir", bg="#e74c3c", fg="white", command=exit_application, height=2, width=10)
exit_button.grid(row=2, column=0, sticky=SE, padx=10, pady=10)

main.mainloop()