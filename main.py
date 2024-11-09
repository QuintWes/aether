from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app_data import board_members_years

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    active = 'main'
    return templates.TemplateResponse("main.html", {"request": request, "active": active})

@app.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    active = 'main'
    return templates.TemplateResponse("main.html", {"request": request, "active": active})

@app.get("/board_members", response_class=HTMLResponse)
async def board_members_page(request: Request):
    active = 'board_members'
    return templates.TemplateResponse("board_members.html", {"request": request, "board_members_years": board_members_years, "active": active})


@app.get("/{page}", response_class=HTMLResponse)
async def fallback_page(request: Request, page: str):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
