from fastapi import UploadFile,APIRouter

app03=APIRouter()


@app03.post("/uploadfile")
async def getfile(file:UploadFile):

    return{
        "file":file.filename
    }