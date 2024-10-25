# DownloadMaster 1.0

DownloadMaster 1.0 es una aplicación que te ayuda a descargar fácilmente archivos de audio y video desde YouTube. Su principal ventaja es que cuenta con una interfaz gráfica amigable, fácil de usar y personalizable.

## Descripción
Esta aplicación te permite descargar tanto audio como video de YouTube. Puedes elegir la calidad de las descargas y el lugar donde deseas guardar los archivos. Además, ofrece algunas características interesantes como la barra de progreso y mensajes que te indican cómo va la descarga.

## Características principales
- **Descarga de audio y video**: La aplicación permite descargar archivos en diferentes formatos, tanto de audio como de video.
- **Selección de calidad**: Puedes elegir la calidad del audio (320kbps, 256kbps, 160kbps) y del video (1080p, 720p, 480p, 360p).
- **Barra de progreso**: Mientras se descargan los archivos, se muestra una barra de progreso para que sepas cuánto falta.
- **Mensajes de estado**: Estos mensajes te informan cuando la descarga ha comenzado, cómo va avanzando y si ha terminado o si ocurrió algún error.
- **Selección de directorio**: Te permite seleccionar la carpeta donde deseas guardar los archivos descargados.
- **Interfaz personalizable**: Puedes cambiar el título de la aplicación y también su icono.

## Requisitos
- **Python 3.x**: Necesitas tener instalado Python en tu computadora.
- **Bibliotecas necesarias**: Las bibliotecas necesarias son `tkinter`, `pytube` y `ttkthemes` (esta última es opcional si quieres aplicar temas a la interfaz).

## Instalación
Para instalar la aplicación, sigue estos pasos:

1. **Clona el repositorio**: Para empezar, tienes que clonar el repositorio desde GitHub con el siguiente comando:
    ```bash
    git clone https://tu-repositorio.git
    ```

2. **Instala las dependencias**: Luego, instala las bibliotecas necesarias con el siguiente comando:
    ```bash
    pip install tkinter pytube ttkthemes
    ```

    *Nota*: La biblioteca `ttkthemes` es opcional, pero te permitirá aplicar diferentes temas a la interfaz de la aplicación.

## Uso
Para usar la aplicación, sigue estos pasos sencillos:

1. Ejecuta el script principal (`main.py`):
    ```bash
    python main.py
    ```

2. Pega la **URL del video de YouTube** que quieres descargar en el campo correspondiente.

3. Selecciona la **calidad de audio o video** que prefieras.

4. Haz clic en el botón **Descargar Audio** o **Descargar Video**.

5. Si es necesario, elige la **carpeta de destino** donde se guardará el archivo.

## Código (Fragmento)
Este es un fragmento del código que se usa para descargar el audio de un video de YouTube:

```python
def download_audio(link, audio_path):
    """
    Descarga un archivo de audio desde YouTube.

    Args:
        link: La URL del video de YouTube.
        audio_path: La ruta donde se guardará el archivo de audio.
    """
    try:
        # Aquí iría el código para descargar el audio
    except Exception as e:
        # Aquí se manejarían los errores
        print(f"Error al descargar: {e}")
```

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes alguna sugerencia de mejora, por favor abre un issue o envía un pull request.  
Cualquier persona es completamente libre de hacer mejoras al código. Si tienes alguna idea que pueda mejorar la aplicación, no dudes en compartirla.

## Presenta: 
Samuel Mena Pupiales (Sam100uel@gmail.com)
