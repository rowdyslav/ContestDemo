import httpx
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from icecream import ic

app = FastAPI()
templates = Jinja2Templates(directory="templates")
static = StaticFiles(directory="static")
app.mount("/static", static, name="static")

URL = "http://127.0.0.1:8000"


@app.get("/")
async def index(request: Request):
    async with httpx.AsyncClient() as client:
        responce = await client.get(f"{URL}/projects/list/")
        projects = responce.json()["value"]
    return templates.TemplateResponse(
        request, "index.html", context={"projects": projects}
    )
