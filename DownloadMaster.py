import os
from tkinter import *
from tkinter import filedialog, font, ttk
from PIL import Image, ImageTk
from urllib.request import urlretrieve
from pytube import YouTube
import threading
import time
import pygetwindow as gw
from tkinter import PhotoImage
from ttkthemes import ThemedTk

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
                urlretrieve(stream.url, video_file_path, reporthook=update_progress_bar)
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

    AUDIO_PATH = os.path.abspath(os.path.join(selected_directory, "Descargas"))
    VIDEO_PATH = os.path.abspath(os.path.join(selected_directory, "Descargas"))

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

main = Tk()
main.title("BRELoad")
main.config(bg="#2c3e50") 
main.wm_state('zoomed') # Cambia el color de fondo a tu preferencia

estado = StringVar()

FRAME_MAIN = Frame(bg="#2c3e50")  # Cambia el color de fondo a tu preferencia
FRAME_MAIN.pack(ipadx=10, pady=10)

MENSAJE = Label(FRAME_MAIN, bg="#2c3e50", fg="white", font=("arial", 12, "bold"))
MENSAJE.pack()

Frame(FRAME_MAIN, height=50, bg="#2c3e50").pack()

Label(FRAME_MAIN, text="➤DOWNLOADMASTER", fg="white", bg="red", height=2, width=20, font=("arial", 12, "bold")).pack(ipadx=10, ipady=10)

Label(FRAME_MAIN, text="PEGA EL LINK (AUDIO):", bg="#2c3e50", fg="white").pack(pady=(20, 0))

LINK = Entry(FRAME_MAIN, width=50, relief=SOLID, highlightthickness=2, highlightcolor="white")
LINK.pack(ipady=5)
LINK.focus_set()

calidad_audio_var = StringVar()
calidad_audio_var.set("192kbps")

calidad_audio_frame = Frame(FRAME_MAIN, bg="#2c3e50")
calidad_audio_frame.pack(pady=(10, 0))

Label(calidad_audio_frame, text="Calidad de Audio:", bg="#2c3e50", fg="white").pack(side=LEFT)

calidades_audio = ["192kbps", "256kbps", "320kbps"]
for calidad in calidades_audio:
    Radiobutton(calidad_audio_frame, text=calidad, variable=calidad_audio_var, value=calidad, bg="#2c3e50", fg="white").pack(side=LEFT)

AUDIO_DOWNLOAD = Button(FRAME_MAIN, text="DESCARGAR AUDIO", bg="lightblue", cursor="hand2", command=lambda: threading.Thread(target=download_audio, args=(LINK.get(), AUDIO_PATH)).start())
AUDIO_DOWNLOAD.pack(pady=(10, 0))

Frame(FRAME_MAIN, height=50, bg="#2c3e50").pack()

Label(FRAME_MAIN, text="➤DOWNLOADMASTER", fg="white", bg="red", height=2, width=20, font=("arial", 12, "bold")).pack(ipadx=10, ipady=10)
Label(FRAME_MAIN, text="PEGA EL LINK (VIDEO):", bg="#2c3e50", fg="white").pack(pady=(20, 0))

LINK_VIDEO = Entry(FRAME_MAIN, width=50, relief=SOLID, highlightthickness=2, highlightcolor="white")
LINK_VIDEO.pack(ipady=5)

calidad_video_var = StringVar()
calidad_video_var.set("720p")

calidad_video_frame = Frame(FRAME_MAIN, bg="#2c3e50")
calidad_video_frame.pack(pady=(10, 0))

Label(calidad_video_frame, text="Calidad de Video:", bg="#2c3e50", fg="white").pack(side=LEFT)

calidades_video = ["1080p", "720p", "480p", "360p"]
for calidad in calidades_video:
    Radiobutton(calidad_video_frame, text=calidad, variable=calidad_video_var, value=calidad, bg="#2c3e50", fg="white").pack(side=LEFT)

DOWNLOAD = Button(FRAME_MAIN, text="DESCARGAR VIDEO", bg="lightgreen", cursor="hand2", command=lambda: threading.Thread(target=download_video, args=(LINK_VIDEO.get(), VIDEO_PATH)).start())
DOWNLOAD.pack(padx=10, pady=(20, 0))

Frame(FRAME_MAIN, height=10, bg="#2c3e50").pack()

OPEN_DIR_VIDEO = Button(FRAME_MAIN, text="📂", bg="yellow", cursor="hand2", command=lambda: os.startfile(VIDEO_PATH))
OPEN_DIR_VIDEO.pack(side=LEFT, pady=(10, 0))

CHOOSE_DIR = Button(FRAME_MAIN, text="ELEGIR RUTA DE DESCARGA", bg="orange", cursor="hand2", command=select_download_directory)
CHOOSE_DIR.pack(side=LEFT, pady=(10, 0))

PROGRESS_BAR = ttk.Progressbar(FRAME_MAIN, length=500, mode="determinate")
PROGRESS_BAR.pack(pady=(10, 20))
PROGRESS_BAR.start_time = time.time()

exit_button = Button(main, text="Salir", bg="red", fg="white", command=exit_application, height=2, width=10)
exit_button.pack(side="bottom", anchor="se", padx=10, pady=10)

font_size = 12
mono_font = font.Font(family='Courier New', size=font_size)

main.mainloop()
import os
from tkinter import *
from tkinter import filedialog, font, ttk
from PIL import Image, ImageTk
from urllib.request import urlretrieve
from pytube import YouTube
import threading
import time
import pygetwindow as gw
from tkinter import PhotoImage
from ttkthemes import ThemedTk

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
                urlretrieve(stream.url, video_file_path, reporthook=update_progress_bar)
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

    AUDIO_PATH = os.path.abspath(os.path.join(selected_directory, "Descargas"))
    VIDEO_PATH = os.path.abspath(os.path.join(selected_directory, "Descargas"))

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

main = Tk()
main.title("BRELoad")
main.config(bg="#2c3e50") 
main.wm_state('zoomed') # Cambia el color de fondo a tu preferencia

estado = StringVar()

FRAME_MAIN = Frame(bg="#2c3e50")  # Cambia el color de fondo a tu preferencia
FRAME_MAIN.pack(ipadx=10, pady=10)

MENSAJE = Label(FRAME_MAIN, bg="#2c3e50", fg="white", font=("arial", 12, "bold"))
MENSAJE.pack()

Frame(FRAME_MAIN, height=50, bg="#2c3e50").pack()

Label(FRAME_MAIN, text="➤DOWNLOADMASTER", fg="white", bg="red", height=2, width=20, font=("arial", 12, "bold")).pack(ipadx=10, ipady=10)

Label(FRAME_MAIN, text="PEGA EL LINK (AUDIO):", bg="#2c3e50", fg="white").pack(pady=(20, 0))

LINK = Entry(FRAME_MAIN, width=50, relief=SOLID, highlightthickness=2, highlightcolor="white")
LINK.pack(ipady=5)
LINK.focus_set()

calidad_audio_var = StringVar()
calidad_audio_var.set("192kbps")

calidad_audio_frame = Frame(FRAME_MAIN, bg="#2c3e50")
calidad_audio_frame.pack(pady=(10, 0))

Label(calidad_audio_frame, text="Calidad de Audio:", bg="#2c3e50", fg="white").pack(side=LEFT)

calidades_audio = ["192kbps", "256kbps", "320kbps"]
for calidad in calidades_audio:
    Radiobutton(calidad_audio_frame, text=calidad, variable=calidad_audio_var, value=calidad, bg="#2c3e50", fg="white").pack(side=LEFT)

AUDIO_DOWNLOAD = Button(FRAME_MAIN, text="DESCARGAR AUDIO", bg="lightblue", cursor="hand2", command=lambda: threading.Thread(target=download_audio, args=(LINK.get(), AUDIO_PATH)).start())
AUDIO_DOWNLOAD.pack(pady=(10, 0))

Frame(FRAME_MAIN, height=50, bg="#2c3e50").pack()

Label(FRAME_MAIN, text="➤DOWNLOADMASTER", fg="white", bg="red", height=2, width=20, font=("arial", 12, "bold")).pack(ipadx=10, ipady=10)
Label(FRAME_MAIN, text="PEGA EL LINK (VIDEO):", bg="#2c3e50", fg="white").pack(pady=(20, 0))

LINK_VIDEO = Entry(FRAME_MAIN, width=50, relief=SOLID, highlightthickness=2, highlightcolor="white")
LINK_VIDEO.pack(ipady=5)

calidad_video_var = StringVar()
calidad_video_var.set("720p")

calidad_video_frame = Frame(FRAME_MAIN, bg="#2c3e50")
calidad_video_frame.pack(pady=(10, 0))

Label(calidad_video_frame, text="Calidad de Video:", bg="#2c3e50", fg="white").pack(side=LEFT)

calidades_video = ["1080p", "720p", "480p", "360p"]
for calidad in calidades_video:
    Radiobutton(calidad_video_frame, text=calidad, variable=calidad_video_var, value=calidad, bg="#2c3e50", fg="white").pack(side=LEFT)

DOWNLOAD = Button(FRAME_MAIN, text="DESCARGAR VIDEO", bg="lightgreen", cursor="hand2", command=lambda: threading.Thread(target=download_video, args=(LINK_VIDEO.get(), VIDEO_PATH)).start())
DOWNLOAD.pack(padx=10, pady=(20, 0))

Frame(FRAME_MAIN, height=10, bg="#2c3e50").pack()

OPEN_DIR_VIDEO = Button(FRAME_MAIN, text="📂", bg="yellow", cursor="hand2", command=lambda: os.startfile(VIDEO_PATH))
OPEN_DIR_VIDEO.pack(side=LEFT, pady=(10, 0))

CHOOSE_DIR = Button(FRAME_MAIN, text="ELEGIR RUTA DE DESCARGA", bg="orange", cursor="hand2", command=select_download_directory)
CHOOSE_DIR.pack(side=LEFT, pady=(10, 0))

PROGRESS_BAR = ttk.Progressbar(FRAME_MAIN, length=500, mode="determinate")
PROGRESS_BAR.pack(pady=(10, 20))
PROGRESS_BAR.start_time = time.time()

exit_button = Button(main, text="Salir", bg="red", fg="white", command=exit_application, height=2, width=10)
exit_button.pack(side="bottom", anchor="se", padx=10, pady=10)

font_size = 12
mono_font = font.Font(family='Courier New', size=font_size)

main.mainloop()
