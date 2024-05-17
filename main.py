from fastapi import FastAPI,Response
import httpx
import urllib.parse
from fake_useragent import UserAgent
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set it to ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
@app.get("/redirect")
async def redirectProxy(url:str=None):
    if url is None:
        return Response(status_code=404)
    else:
        ua = UserAgent()
        url = urllib.parse.unquote(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={'User-Agent':ua.random.strip()},follow_redirects=False)
            redirect = response.headers.get("Location") if response.headers else ""
            return Response(content=redirect, media_type="text/html")
