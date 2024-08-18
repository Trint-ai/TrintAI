"""Main application."""

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from huggingface_hub import hf_hub_download, snapshot_download
from core.main import core
from core.config import settings


def load_environment_variables():
    """TODO"""
    # Load environment variables
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    dotenv_path = os.path.join(project_root, settings.ENVIRONMENT_VARIABLES_FILE)
    load_dotenv(dotenv_path=dotenv_path)

def load_hf_models():
    """Pull HF models at start"""
    # TODO: This should be improved

    # Pull emotion model
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="config.json")
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="tf_model.h5")
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="tokenizer_config.json")
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="vocab.json")
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="merges.txt")
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="tokenizer.json")
    hf_hub_download(repo_id=settings.EMOTIONS_MODEL, filename="special_tokens_map.json")

    # Pull whisper model
    hf_hub_download(repo_id=settings.WHISPER_MODEL, filename="config.json")
    hf_hub_download(repo_id=settings.WHISPER_MODEL, filename="vocabulary.json")
    hf_hub_download(repo_id=settings.WHISPER_MODEL, filename="preprocessor_config.json")
    hf_hub_download(repo_id=settings.WHISPER_MODEL, filename="tokenizer.json")
    hf_hub_download(repo_id=settings.WHISPER_MODEL, filename="preprocessor_config.json")
    hf_hub_download(repo_id=settings.WHISPER_MODEL, filename="model.bin")

class Api(BaseModel):
    file: str


app = FastAPI(title="TrintAI API", version="0.0.1")


@app.post("/api")
async def api(item: Api):
    body = item.model_dump()
    trintai = core(body['file'])
    result = trintai.start()

    if result is None:
        return Response(status_code=500)
    else:
        return JSONResponse(content=result)

if __name__ == '__main__':
    load_environment_variables()
    load_hf_models()
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)
