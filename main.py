from fastapi import FastAPI, Response
import httpx
import urllib.parse
from fake_useragent import UserAgent
import random  # Import random module
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
import json
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
        # proxies_response = httpx.get("https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=speed&sort_type=asc")  # Changed variable name to avoid overwriting 'proxies'
        # proxies_data = proxies_response.json()  # Extract JSON data from response
        # socks4_proxies = [entry for entry in proxies_data["data"] if 'socks5' in entry.get('protocols', [])]

        # random_socks4_proxy = random.choice(socks4_proxies)
        # socks4_ip = random_socks4_proxy['ip']
        # socks4_port = random_socks4_proxy['port']
        # proxy = f"socks5://{socks4_ip}:{socks4_port}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={'User-Agent': ua.random.strip()}, follow_redirects=False) 
            redirect = response.headers.get("Location") if response.headers else ""
            print(response.text)
            return Response(content=redirect, media_type="text/html")
@app.get("/metaproxy")
async def meta_proxy(destination:str=None):  # Corrected function name to follow naming conventions
    url = destination
    if url is None:
        return Response(status_code=404)
    else:
        ua = UserAgent()
        url = urllib.parse.unquote(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={
                'User-Agent': ua.random.strip(),
                # 'Accept': 'application/json, text/javascript, */*; q=0.01',
                # 'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.primewire.tf/links/go/GYP73',
                # 'TE': 'trailers'
            },follow_redirects=True) 
            return Response(content=response.text, media_type="application/json")
@app.post("/fileproxy")
async def meta_proxy_post(url:str=None,data:str=None):  # Corrected function name to follow naming conventions
    if url is None:
        return Response(status_code=404)
    else:
        ua = UserAgent()
        url = urllib.parse.unquote(url)
        data = json.loads(urllib.parse.unquote(data))
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers={
                'User-Agent': ua.random.strip(),
                'Accept': 'text/html',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.febbox.com/',
                'TE': 'trailers'
            },data=data) 
            return Response(content=response.text, media_type="text/html")
