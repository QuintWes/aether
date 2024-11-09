from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app_data import board_members_years
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

PROJECT_DIR = os.getenv("PROJECT_DIR")

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

@app.post("/git-webhook")
async def git_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    # Check if the webhook event is a push to the main branch
    if payload.get("ref") == "refs/heads/main":
        # Run the update script in the background
        background_tasks.add_task(update_repository)
        
    return {"message": "Webhook received"}

def update_repository():
    print("Starting update_repository function")
    # Define the full path to the script inside the /aether folder, wrapped in quotes
    script_path = "/home/quint/python projects/aether/update_and_restart.sh"
    
    # Use 'bash' to execute the script with the path wrapped in double quotes
    result = subprocess.run(f'bash "{script_path}"', shell=True, capture_output=True, text=True)
    
    print(f"Script output: {result.stdout}")
    if result.stderr:
        print(f"Script error: {result.stderr}")