from fastapi import FastAPI

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

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
