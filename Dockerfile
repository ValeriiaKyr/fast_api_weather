# używa lekkiego obrazu bazowego z Pythonem 3.12 (wersja slim dla mniejszego rozmiaru)
FROM python:3.12-slim

# ustawia katalog roboczy wewnątrz kontenera na /app
WORKDIR /app

# kopiuje plik requirements.txt z lokalnego katalogu do kontenera
COPY requirements.txt .

# instaluje wszystkie zależności z pliku requirements.txt bez buforowania
RUN pip install --no-cache-dir -r requirements.txt

# kopiuje pozostałe pliki projektu do katalogu roboczego w kontenerze
COPY . .

# uruchamia serwer aplikacji FastAPI przy użyciu uvicorn
# --host 0.0.0.0 pozwala na dostęp spoza kontenera
# --port 8000 ustawia port aplikacji
# --reload automatycznie przeładowuje aplikację przy zmianach kodu (tryb deweloperski)
CMD ["uvicorn", "weather.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
