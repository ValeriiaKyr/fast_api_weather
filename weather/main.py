import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.v1.routes import router

app = FastAPI()
app.include_router(router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="weather/static"), name="static")
templates = Jinja2Templates(directory="weather/templates")


@app.get("/", response_class=HTMLResponse)
def get_city_list(request: Request, start_date: str = None, end_date: str = None):
    api_url = "http://127.0.0.1:8000/api/v1/cities-scores/"
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        cities = response.json()
    except Exception:
        cities = []

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cities": cities,
            "start_date": start_date,
            "end_date": end_date,
        },
    )
