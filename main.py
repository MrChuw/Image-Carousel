import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

from pydantic import BaseModel

from schemas import URLList
from utils import api_key_required, save_url_list
from textwrap import dedent


class URLListSchema(BaseModel):
    urls: list[str]


app = FastAPI()
register_tortoise(app, db_url="sqlite://db.sqlite3", modules={"models": ["schemas"]}, generate_schemas=True,
                  add_exception_handlers=True)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
async def get_favicon():
    return app.url_path_for('static', path='favicon.gif')


@app.get("/robots.txt", response_class=PlainTextResponse)
async def get_robot():
    return dedent("""
    User-agent: *
    Disallow: /
    """).lstrip("\n")


@app.post("/upload")
async def add_urls(request: Request, data: URLListSchema, api_key: str = Depends(api_key_required)):
    urls = data.urls
    if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
        raise HTTPException(status_code=400, detail="URLs must be a list of strings")
    uuid_obj = uuid.uuid4()
    url = uuid_obj.hex[:16]
    await save_url_list(urls, url)
    return JSONResponse(content={"success": f"{request.url_for('get_urls', post_id=url)}"}, status_code=201)


@app.get("/{post_id}", response_class=HTMLResponse)
async def get_urls(request: Request, post_id: str):
    url_list = await URLList.get_or_none(url_list=post_id).prefetch_related("urls")
    if not url_list:
        raise HTTPException(status_code=404, detail="URL does not exist.")
    urls = await url_list.urls
    urls_list = [url.url for url in urls]
    return templates.TemplateResponse("urls_template.html",
                                      {"request": request, "urls": urls_list, "urls_count": len(urls)}
                                      )


if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", workers=4)
