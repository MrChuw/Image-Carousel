from fastapi import HTTPException, Request

from schemas import APIKey, URL, URLList


async def save_url_list(url_strings: list[str], list_url: str):
    url_list, created = await URLList.get_or_create(url_list=list_url)
    for url_string in url_strings:
        url, created = await URL.get_or_create(url=url_string)
        await url_list.urls.add(url)


async def api_key_required(request: Request):
    api_key = request.headers.get('x-api-key')
    if not api_key:
        raise HTTPException(status_code=401, detail="API key is missing")
    valid_key = await APIKey.get_or_none(key=api_key, is_active=True)
    if not valid_key:
        raise HTTPException(status_code=403, detail="Invalid or inactive API key")
    return valid_key
