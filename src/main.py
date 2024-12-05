import os
import yt_dlp
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Query, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates




app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('/static', StaticFiles(directory=static_path), 'static')

templates = Jinja2Templates(directory=templates_path)


@app.get('/', tags=['home'])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome'})


@app.post('/download', response_class=JSONResponse)
async def download_video(url: str = Form(...)):
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
        raise HTTPException(
            status_code=500, detail=f"Error al descargar el video: {str(e)}")
