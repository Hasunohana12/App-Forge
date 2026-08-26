import requests

PROJECT_REF = "flyznurbkihesnylrwov"
API_KEY = "sb_publishable_E7bpFRnKfmdcV8ouIUEJrQ_tDUxF2sF"
BASE_URL = f"https://{PROJECT_REF}.supabase.co/rest/v1"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def obtener_clientes():
    response = requests.get(f"{BASE_URL}/cliente?select=*", headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def obtener_aplicaciones():
    response = requests.get(f"{BASE_URL}/aplicacion?select=*,cliente(*)", headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def obtener_desarrolladores():
    response = requests.get(f"{BASE_URL}/desarrollador?select=*", headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def obtener_detalles_proyecto():
    url = f"{BASE_URL}/desarrolladopordetalle?select=*,desarrollador(*),aplicacion(*)"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []