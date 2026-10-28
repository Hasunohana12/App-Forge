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

def asignar_dev_a_proyecto(id_app, id_dev, rol="Desarrollador", horas=0):
    try:
        body_relacion = {
            "id_app": int(id_app),
            "id_desarrollador": int(id_dev),
            "rol_desempenado": rol,
            "horas_dedicadas": int(horas) if horas else 0
        }
        requests.post(f"{BASE_URL}/desarrollador_aplicacion", json=body_relacion, headers=HEADERS)

        url_app = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
        body_app = {
            "estado": "ASIGNADO"
        }
        res = requests.patch(url_app, json=body_app, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al asignar dev a proyecto: {e}")
        return False

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

def obtener_desarrollador_por_id(id_dev):
    try:
        url = f"{BASE_URL}/desarrollador?id_desarrollador=eq.{id_dev}"
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200 and len(res.json()) > 0:
            return res.json()[0]
        return None
    except Exception as e:
        print(f"Error al obtener desarrollador por ID: {e}")
        return None

def actualizar_desarrollador(id_dev, nombre_completo, especialidad, email):
    body = {
        "nombre_completo": nombre_completo,
        "especialidad": especialidad,
        "email": email
    }
    try:
        url = f"{BASE_URL}/desarrollador?id_desarrollador=eq.{id_dev}"
        res = requests.patch(url, json=body, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al actualizar desarrollador: {e}")
        return False

def eliminar_desarrollador(id_dev):
    try:
        url = f"{BASE_URL}/desarrollador?id_desarrollador=eq.{id_dev}"
        res = requests.delete(url, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al eliminar desarrollador: {e}")
        return False