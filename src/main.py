from fastapi import FastAPI
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import yt_dlp

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('static/', StaticFiles(directory=static_path), 'static')

templates=Jinja2Templates(directory=templates_path)

@app.get('/download', response_class=JSONResponse)
async def download_video(url: str = Query(..., description="URL del video de YouTube a descargar")):
    # Opciones de configuración para yt_dlp
    yt_opts = {
        'format': 'bestvideo+bestaudio/best',  # Requiere FFMPEG
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    try:
        # Descargar el video usando yt_dlp
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([url])
        
        return {"message": "Descarga completada", "url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el video: {str(e)}")
