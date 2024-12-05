from fastapi import FastAPI
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    """
    Zobrazí formulář na úvodní stránce.
    """
    return templates.TemplateResponse("index_password_cracking.html", {"request": request})