from fastapi import APIRouter,Request

app04=APIRouter()

@app04.post("/request")
async def request(request:Request):
    print("url:",request.url)
    print("客户ip:",request.client.host)
    print("客户端宿主",request.headers.get("user-agent"))
    print("cookies:",request.cookies)
    return{
        "url":request.url,
        "客户ip":request.client.host,
        "客户端宿主":request.headers.get("user-agent"),
        "cookies:":request.cookies
    }