from fastapi import FastAPI, Response
import httpx
import urllib.parse
from fake_useragent import UserAgent
import random  # Import random module
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
async def redirect_proxy(url:str=None):  # Corrected function name to follow naming conventions
    if url is None:
        return Response(status_code=404)
    else:
        ua = UserAgent()
        url = urllib.parse.unquote(url)
        proxies_response = httpx.get("https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=speed&sort_type=asc")  # Changed variable name to avoid overwriting 'proxies'
        proxies_data = proxies_response.json()  # Extract JSON data from response
        socks4_proxies = [entry for entry in proxies_data["data"] if 'socks5' in entry.get('protocols', [])]

        random_socks4_proxy = random.choice(socks4_proxies)
        socks4_ip = random_socks4_proxy['ip']
        socks4_port = random_socks4_proxy['port']
        proxy = f"socks5://{socks4_ip}:{socks4_port}"
        async with httpx.AsyncClient(proxy=proxy) as client:  # Changed variable name to avoid overwriting 'proxies'
            response = await client.get(url, headers={'User-Agent': ua.random.strip()}, follow_redirects=False)  # Changed variable name to avoid overwriting 'response'
            redirect = response.headers.get("Location") if response.headers else ""
            print(response.text)
            return Response(content=redirect, media_type="text/html")
