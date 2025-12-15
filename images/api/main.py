from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
import psycopg2
import os
import logging

from security import hash_password, verify_password

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # nginx proxy → safe
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ----------------
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# ---------------- DB ----------------
def get_conn():
    logger.info("Connecting to PostgreSQL")
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )

# ---------------- JWT ----------------
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = "HS256"
JWT_EXPIRE = int(os.getenv("JWT_EXPIRE_MINUTES", 30))

security = HTTPBearer()

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def get_current_user(
    creds: HTTPAuthorizationCredentials = Security(security)
):
    try:
        payload = jwt.decode(
            creds.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALG]
        )
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")

# ---------------- ROUTES ----------------
@app.post("/register")
def register(user: UserRegister):
    conn = get_conn()
    cur = conn.cursor()

    logger.info("Attempting user registration")

    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (user.username, hash_password(user.password))
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="username already exists")
    finally:
        cur.close()
        conn.close()

    return {"message": "user registered"}

@app.post("/login")
def login(user: UserLogin):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM users WHERE username = %s",
        (user.username,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row or not verify_password(user.password, row[0]):
        logger.warning("Invalid login attempt")
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_token(user.username)
    logger.info(f"User {user.username} logged in")

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}

@app.get("/health")
def health():
    return {"status": "healthy"}
