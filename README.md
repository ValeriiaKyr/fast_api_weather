# 🌦️ Weather Score App

Aplikacja FastAPI, która pobiera dane pogodowe dla wybranych miast z API [Open-Meteo](https://open-meteo.com/) i oblicza wynik pogodowy (`score`) na podstawie temperatury, prędkości wiatru, wilgotności oraz zachmurzenia.  
Wyniki można przeglądać w interfejsie webowym lub za pośrednictwem endpointu API.

---

## 📁 Struktura projektu

```bash
weather/
├── api/
│   └── v1/
│       └── routes.py          # Główne endpointy API
├── models/
│   └── schemas.py             # Schematy danych Pydantic
├── services/
│   └── weather_service.py     # Logika pobierania danych pogodowych
├── static/
│   └── style.css              # Style dla GET /
├── utils/
│   └── metrics.py             # Obliczanie wyników pogodowych
├── templates/
│   └── index.html             # Szablon strony głównej
├── tests/
│   └── test_weather_api.py    # Testy GET /api/v1/cities-scores
├── static/                    # Pliki statyczne (CSS)
└── main.py                    # Punkt wejścia aplikacji FastAPI
```
## Instalacja i uruchomienie (lokalnie)

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/ValeriiaKyr/fast_api_weather.git
```

### 2. Utworzenie środowiska wirtualnego

```bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchomienie serwera

```bash
uvicorn weather.main:app --reload
```

## 💻 Użycie

---

### 🌍 Interfejs webowy

Przejdź do:  
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**  

Aby zobaczyć listę miast z ich wynikami pogodowymi.  
Możesz wybrać zakres dat, aby przeliczyć wyniki dla innego okresu.

---

### 📡 Endpoint API

#### `GET /api/v1/cities-scores/`

---

#### ⚙️ Parametry opcjonalne:

| Parametr     | Typ   | Opis                                 | Format        |
|---------------|--------|--------------------------------------|----------------|
| `start_date`  | string | Data początkowa                      | `YYYY-MM-DD`   |
| `end_date`    | string | Data końcowa                        | `YYYY-MM-DD`   |

> Jeśli nie podasz dat, zostanie użyty **wczorajszy dzień**.

---

#### Przykład zapytania

```bash
curl "http://127.0.0.1:8000/api/v1/cities-scores/?start_date=2025-10-28&end_date=2025-10-30"
```

## Jak obliczany jest wynik (`score`)

Każde miasto otrzymuje wynik na podstawie **średnich wartości pogodowych** z czterech czynników:

| Czynnik              | Waga | Opis |
|----------------------|------|------|
| **Temperatura**     | 35% | Najlepsza w okolicach **24°C**, odchylenie obniża wynik |
| **Prędkość wiatru** | 20% | Im mniejsza prędkość, tym wyższy wynik |
| **Wilgotność względna** | 20% | Idealna wartość to  **50%** |
| **Zachmurzenie**      | 25% | Najkorzystniejsze przy **25% zachmurzenia** |

Każdy z czynników oceniany jest w skali **0–10**,  
a łączny wynik (`score`) to **średnia ważona** wszystkich czterech.

---

## Uruchomienie w Dockerze

### 1. Budowanie obrazu

```bash
docker build -t weather-score-app .
```

### 2. Uruchomienie kontenera

```bash
docker run -p 8000:8000 weather-score-app
```

### 3. Otwórz w przeglądarce:

Przejdź do:  
👉 **[http://localhost:8000](http://localhost:8000)**  