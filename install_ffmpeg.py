import os
import requests
import zipfile
import shutil
import sys
from pathlib import Path
import subprocess

def install_ffmpeg():
    print("Instalando FFmpeg para Windows...")
    
    # Directorio donde se guardarán los archivos de FFmpeg
    ffmpeg_dir = Path(os.path.expanduser("~")) / "ffmpeg"
    ffmpeg_bin = ffmpeg_dir / "bin"
    
    # Crear directorio si no existe
    os.makedirs(ffmpeg_dir, exist_ok=True)
    
    # URL para descargar FFmpeg
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = ffmpeg_dir / "ffmpeg.zip"
    
    print("Descargando FFmpeg desde GitHub...")
    
    # Descargar el archivo zip
    try:
        response = requests.get(ffmpeg_url, stream=True)
        response.raise_for_status()
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"Error al descargar FFmpeg: {e}")
        return False
    
    print("Extrayendo archivos...")
    
    # Extraer el zip
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Encontrar el directorio extraído (puede tener un nombre específico con versión)
        extracted_dirs = [d for d in os.listdir(ffmpeg_dir) if os.path.isdir(os.path.join(ffmpeg_dir, d)) and d.startswith("ffmpeg")]
        
        if extracted_dirs:
            extracted_dir = os.path.join(ffmpeg_dir, extracted_dirs[0])
            
            # Mover el contenido del directorio bin
            if os.path.exists(os.path.join(extracted_dir, "bin")):
                if os.path.exists(ffmpeg_bin):
                    shutil.rmtree(ffmpeg_bin)
                shutil.copytree(os.path.join(extracted_dir, "bin"), ffmpeg_bin)
        else:
            print("No se encontró el directorio extraído.")
            return False
    except Exception as e:
        print(f"Error al extraer FFmpeg: {e}")
        return False
    
    # Eliminar archivos temporales
    try:
        os.remove(zip_path)
        for dir_name in extracted_dirs:
            shutil.rmtree(os.path.join(ffmpeg_dir, dir_name))
    except Exception as e:
        print(f"Error al limpiar archivos temporales: {e}")
    
    print(f"FFmpeg instalado en: {ffmpeg_bin}")
    
    # Agregar al PATH para esta sesión
    if ffmpeg_bin.exists():
        os.environ["PATH"] = f"{ffmpeg_bin};{os.environ['PATH']}"
        print("FFmpeg ha sido añadido al PATH temporalmente para esta sesión.")
        
        # Verificar instalación
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("FFmpeg instalado correctamente:")
                print(result.stdout.splitlines()[0])
                return True
            else:
                print("FFmpeg se instaló pero no se puede ejecutar.")
                return False
        except Exception as e:
            print(f"Error al verificar la instalación: {e}")
            return False
    else:
        print(f"El directorio {ffmpeg_bin} no existe después de la instalación.")
        return False

if __name__ == "__main__":
    success = install_ffmpeg()
    if success:
        print("\nPara usar FFmpeg permanentemente, debes añadir esta ruta a tu PATH:")
        print(f"   {Path(os.path.expanduser('~')) / 'ffmpeg' / 'bin'}")
        print("\nAhora puedes ejecutar el programa principal con:")
        print("   python app.py")
    else:
        print("\nLa instalación de FFmpeg falló. Por favor, instálalo manualmente siguiendo las instrucciones en el README.") 