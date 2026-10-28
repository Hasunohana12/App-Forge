import os
import requests

PROJECT_REF = os.getenv('SUPABASE_URL', 'https://flyznurbkihesnylrwov.supabase.co').replace('https://', '').replace('.supabase.co', '')
API_KEY = os.getenv('SUPABASE_KEY', 'sb_publishable_E7bpFRnkfmdcV8ouIUEJrQ_tDUxF2sF')
BASE_URL = f"https://{PROJECT_REF}.supabase.co/rest/v1"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def obtener_desarrolladores():
    try:
        url = f"{BASE_URL}/desarrollador?select=*"
        response = requests.get(url, headers=HEADERS)
        
        print("=== DEBUG SUPABASE GET ===")
        print("URL:", url)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)
        print("=========================")

        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error en obtener_desarrolladores: {e}")
        return []

def asignar_dev_a_proyecto(id_app, id_desarrollador, rol, horas):
    body = {
        "id_app": int(id_app),
        "id_desarrollador": int(id_desarrollador),
        "rol": rol,
        "horas_dedicadas": int(horas) if horas else 0
    }
    requests.post(f"{BASE_URL}/desarrolladorpordetalle", json=body, headers=HEADERS)
    
    patch_url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
    requests.patch(patch_url, json={"estado": "ASIGNADO"}, headers=HEADERS)

def obtener_proyectos_por_dev(id_desarrollador):
    url = f"{BASE_URL}/desarrolladorpordetalle?select=rol,horas_dedicadas,aplicacion(nombre,estado)&id_desarrollador=eq.{id_desarrollador}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def crear_nuevo_desarrollador(nombre_completo, especialidad, email, contrasena=None):
    body = {
        "nombre_completo": nombre_completo,
        "especialidad": especialidad,
        "email": email,
        "disponible": True,
        "proyectos_activos": 0,
        "proyectos_completados": 0
    }
    if contrasena:
        body["contrasena"] = contrasena

    response = requests.post(f"{BASE_URL}/desarrollador", json=body, headers=HEADERS)
    
    if response.status_code not in (200, 201):
        print(f"Error al registrar en Supabase ({response.status_code}): {response.text}")
        return None
        
    return response.json()

def obtener_desarrollador_por_credenciales(email, password):
    url = f"{BASE_URL}/desarrollador?email=eq.{email}&contrasena=eq.{password}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        datos = response.json()
        return datos[0] if datos else None
    return None