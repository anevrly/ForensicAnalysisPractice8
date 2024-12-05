from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import random
import string
import time

# Inicializace aplikace
app = FastAPI()

# Povolení CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Povolit všechny zdroje (alternativně můžete omezit na konkrétní domény)
    allow_credentials=True,
    allow_methods=["*"],  # Povolit všechny HTTP metody
    allow_headers=["*"],  # Povolit všechny hlavičky
)

# Cesty k šablonám a statickým souborům
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Generování hesla pro různé úrovně složitosti
PASSWORDS = {    
    0: "5612",
    1: "32276",
    2: "bzcd",
    3: "h4b2",
    4: "z+1c"
}

login_attempts = {}  # Sledování pokusů podle IP

def generate_password(complexity: int) -> str:
    if complexity == 0:  # 4 čísla
        return f"{random.randint(0, 9999):04}"
    elif complexity == 1:  # 5 čísel
        return f"{random.randint(0, 99999):05}"
    elif complexity == 2:  # 4 písmena
        return ''.join(random.choices(string.ascii_lowercase, k=4))
    elif complexity == 3:  # 4 písmena a čísla
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=4))
    elif complexity == 4:  # 4 písmena, čísla a speciální znaky
        chars = string.ascii_lowercase + string.digits + "!@#$%^&*()"
        return ''.join(random.choices(chars, k=4))

@app.post("/generate_password")
async def generate(complexity: int = Form(...)):
    # Generate passwords for all complexities
    for i in range(5):
        password = generate_password(i)
        PASSWORDS[i] = password  # Store the password in the global PASSWORDS dict

    return JSONResponse({"result": "Passwords regenerated"})
    # return JSONResponse({"password": password})



@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    """
    Zobrazí formulář na úvodní stránce.
    """
    return templates.TemplateResponse("index_safe.html", {"request": request})

@app.post("/check_password", response_class=JSONResponse)
async def check_password(
    request: Request, 
    password: str = Form(...), 
    complexity: int = Form(...)
):
    """
    Ověří zadané heslo a aplikuje ochranu proti brute-force.
    """
    client_ip = request.client.host

    # Kontrola pokusů
    if client_ip in login_attempts:
        attempts, last_attempt_time = login_attempts[client_ip]
        # Blokace po překročení limitu pokusů
        if attempts >= 5 and time.time() - last_attempt_time < 300:
            return JSONResponse({"result": "BLOCKED"})
        elif time.time() - last_attempt_time >= 300:
            login_attempts[client_ip] = [0, time.time()]
    else:
        login_attempts[client_ip] = [0, time.time()]

    # Ověření hesla
    correct_password = PASSWORDS.get(complexity)
    if password == correct_password:
        login_attempts.pop(client_ip, None)  # Reset pokusů při úspěchu
        return JSONResponse({"result": "OK"})
    else:
        # Zaznamenání neúspěšného pokusu
        login_attempts[client_ip][0] += 1
        login_attempts[client_ip][1] = time.time()
        return JSONResponse({"result": "KO", "attempts_left": 5 - login_attempts[client_ip][0]})

