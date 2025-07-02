import warnings
from urllib3.exceptions import NotOpenSSLWarning
# 1. LibreSSL-Warnung unterdrücken
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import requests
from datetime import date, timedelta
from ics import Calendar, Event

# 2. API-Endpoint und Rolling-Window-Parameter (max. 3 Jahre)
API_URL = "https://openholidaysapi.org/SchoolHolidays"
start   = date.today()
end     = start + timedelta(days=365*3)
params  = {
    "countryIsoCode":  "DE",
    "subdivisionCode": "DE-NW",
    "languageIsoCode": "DE",
    "validFrom":       start.isoformat(),
    "validTo":         end.isoformat()
}

# 3. Emoji-Mapping
EMOJI = {
    "Osterferien":      "🥚 Osterferien",
    "Sommerferien":     "☀️ Sommerferien",
    "Herbstferien":     "🍂 Herbstferien",
    "Weihnachtsferien": "❄️ Weihnachtsferien"
}

def fetch_holidays():
    """Ruft bis zu 3 Jahre Ferien-Daten ab."""
    r = requests.get(API_URL, params=params)
    r.raise_for_status()
    return r.json()

def build_calendar(items):
    """Erstellt aus JSON ein ICS-Calendar-Objekt."""
    cal = Calendar()
    for item in items:
        ev = Event()
        ev.begin = item["startDate"]
        ev.end   = str(date.fromisoformat(item["endDate"]) + timedelta(days=1))
        name     = item["name"][0]["text"]
        ev.name  = EMOJI.get(name, name)
        ev.make_all_day()
        cal.events.add(ev)
    return cal

if __name__ == "__main__":
    holidays = fetch_holidays()
    calendar = build_calendar(holidays)
    print(calendar.serialize())

