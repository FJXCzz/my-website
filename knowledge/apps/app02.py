from fastapi import APIRouter,Form


app02 = APIRouter()

@app02.post("/regin")
async def data(username:str=Form(),password:str=Form()):
    print(f"username:{username},passowrd:{password}")
    return{
        "username":username
    }
