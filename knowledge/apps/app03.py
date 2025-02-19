from fastapi import UploadFile,APIRouter, File

app03=APIRouter()


@app03.post("/uploadfile")
async def getfile(file:UploadFile):

    return{
        "file":file.filename
    }

@app03.post("/file")

async def get_file(file:bytes=File()):
    print("file",file)
    return {
        "file":len(file)
    } 
