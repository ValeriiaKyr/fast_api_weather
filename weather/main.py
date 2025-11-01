import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.v1.routes import router

# inicjalizuje aplikację FastAPI
app = FastAPI()

# dołącza router z endpointami API w wersji v1
app.include_router(router, prefix="/api/v1")

# montuje katalog statyczny (np. pliki CSS, obrazy)
app.mount("/static", StaticFiles(directory="weather/static"), name="static")

# inicjalizuje silnik szablonów Jinja2, wskazując katalog z plikami HTML
templates = Jinja2Templates(directory="weather/templates")


@app.get("/", response_class=HTMLResponse)
def get_city_list(
    request: Request, start_date: str = None, end_date: str = None
) -> HTMLResponse:
    """
    Obsługuje żądanie GET na stronie głównej ("/")
    pobiera dane pogodowe miast z endpointu API `/api/v1/cities-scores/`
    i renderuje stronę HTML z wynikami oraz formularzem wyboru dat.

    Jeśli użytkownik nie poda dat, API zwraca dane dla wczorajszego dnia.

    :param request: obiekt żądania FastAPI, wymagany przez Jinja2Templates do renderowania strony
    :param start_date: data początkowa w formacie YYYY-MM-DD, opcjonalna
    :param end_date: data końcowa w formacie YYYY-MM-DD, opcjonalna
    :return: odpowiedź HTML z wygenerowaną stroną (zawierającą dane miast i formularz)
    """

    # adres endpointu API pobierającego dane pogodowe
    api_url = "http://127.0.0.1:8000/api/v1/cities-scores/"

    # przygotowuje parametry zapytania (daty, jeśli podane)
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    try:
        # wysyła zapytanie HTTP GET do API z ewentualnymi parametrami dat
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # podnosi wyjątek, jeśli status != 200
        cities = response.json()  # parsuje dane JSON zwrócone przez API
    except Exception:
        # w przypadku błędu (np. brak połączenia) zwraca pustą listę
        cities = []

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # obiekt żądania (wymagany przez Jinja2)
            "cities": cities,  # lista miast z danymi pogodowymi
            "start_date": start_date,  # wybrana data początkowa (jeśli istnieje)
            "end_date": end_date,  # wybrana data końcowa (jeśli istnieje)
        },
    )
