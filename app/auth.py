from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import psycopg2

router = APIRouter()
config = Config(".env")
oauth = OAuth(config)
router.oauth = oauth

router.oauth.register(
    name='google',
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    conn = psycopg2.connect(
        host=config("DB_HOST"),
        dbname=config("DB_NAME"),
        user=config("DB_USER"),
        password=config("DB_PASS"),
        port=config("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, name TEXT)")
    cur.execute("INSERT INTO users (email, name) VALUES (%s, %s)", (user_info["email"], user_info["name"]))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "User logged in", "user": user_info}
