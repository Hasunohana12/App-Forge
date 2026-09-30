import requests

PROJECT_REF = "flyznurbkihesnylrwov"
API_KEY = "sb_publishable_E7bpFRnKfmdcV8ouIUEJrQ_tDUxF2sF"
BASE_URL = f"https://{PROJECT_REF}.supabase.co/rest/v1"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def obtener_portafolio_publico():
    url = f"{BASE_URL}/aplicacion?select=*&es_publico_portafolio=eq.true"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def obtener_proyecto_por_id(id_app):
    url = f"{BASE_URL}/aplicacion?select=*,cliente(*)&id_app=eq.{id_app}"
    response = requests.get(url, headers=HEADERS)
    datos = response.json() if response.status_code == 200 else []
    return datos[0] if datos else None

def crear_nuevo_proyecto(nombre, descripcion, fecha_inicio, es_publico):
    body = {
        "nombre": nombre,
        "descripcion": descripcion,
        "fecha_inicio": fecha_inicio,
        "es_publico_portafolio": es_publico,
        "estado": "EN_PROGRESO"
    }
    response = requests.post(f"{BASE_URL}/aplicacion", json=body, headers=HEADERS)
    return response.json() if response.status_code in (200, 201) else None