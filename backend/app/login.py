from fastapi import APIRouter,Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from backend.settings import SECRET_KEY, ALGORITHM
from backend.schemas import Token




applogin = APIRouter()




@app.post('/login')
async def login(login_form:OAuth2PasswordRequestForm=Depends()):
    login.form.username