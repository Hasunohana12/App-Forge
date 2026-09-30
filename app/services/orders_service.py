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

def obtener_clientes():
    response = requests.get(f"{BASE_URL}/cliente?select=*", headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def obtener_solicitudes_pendientes():
    url = f"{BASE_URL}/aplicacion?select=id_app,descripcion,estado,cliente(nombre,email)&estado=eq.PENDIENTE"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def obtener_aplicaciones():
    response = requests.get(f"{BASE_URL}/aplicacion?select=*,cliente(*)", headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def crear_solicitud_cliente(nombre, contacto, email, detalles_app):
    body_cliente = {"nombre": nombre, "contacto": contacto, "email": email}
    res_cliente = requests.post(f"{BASE_URL}/cliente", json=body_cliente, headers=HEADERS)
    
    if res_cliente.status_code in (200, 201):
        cliente = res_cliente.json()[0]
        id_cliente = cliente["id_cliente"]
        
        body_app = {
            "nombre": f"Solicitud de {nombre}",
            "descripcion": detalles_app,
            "estado": "PENDIENTE",
            "id_cliente": id_cliente
        }
        res_app = requests.post(f"{BASE_URL}/aplicacion", json=body_app, headers=HEADERS)
        return res_app.json() if res_app.status_code in (200, 201) else None
    return None