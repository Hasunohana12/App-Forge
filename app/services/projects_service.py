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

def obtener_portafolio_publico():
    try:
        url = f"{BASE_URL}/aplicacion?es_publico_portafolio=eq.true&select=*"
        res = requests.get(url, headers=HEADERS)
        return res.json() if res.status_code == 200 else []
    except Exception as e:
        print(f"Error al obtener portafolio publico: {e}")
        return []

def obtener_proyecto_por_id(id_app):
    try:
        url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}&select=*"
        res = requests.get(url, headers=HEADERS)
        data = res.json()
        if res.status_code == 200 and data:
            return data[0]
        return None
    except Exception as e:
        print(f"Error al obtener proyecto por ID: {e}")
        return None

def crear_nuevo_proyecto(nombre, descripcion, fecha_inicio=None, es_publico=True, imagen_url=None):
    body = {
        "nombre": nombre,
        "descripcion": descripcion,
        "estado": "EN_DESARROLLO",
        "es_publico_portafolio": bool(es_publico)
    }
    if fecha_inicio:
        body["fecha_inicio"] = fecha_inicio

    try:
        res = requests.post(f"{BASE_URL}/aplicacion", json=body, headers=HEADERS)
        if res.status_code not in (200, 201):
            print(f"Error POST Supabase ({res.status_code}): {res.text}")
            return None
        return res.json()
    except Exception as e:
        print(f"Excepción en crear_nuevo_proyecto: {e}")
        return None

def crear_nuevo_proyecto_completo(nombre, descripcion, estado, fecha_inicio, es_publico, dev_ids=None, portada=None, paneles=None):
    return crear_nuevo_proyecto(nombre, descripcion, fecha_inicio, es_publico)

def actualizar_proyecto(id_app, nombre, descripcion, estado, fecha_inicio=None, imagen_url=None, es_publico=True):
    url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
    body = {
        "nombre": nombre,
        "descripcion": descripcion,
        "estado": estado,
        "es_publico_portafolio": bool(es_publico)
    }
    if fecha_inicio:
        body["fecha_inicio"] = fecha_inicio
    if imagen_url:
        body["imagen_portada"] = imagen_url

    try:
        res = requests.patch(url, json=body, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al actualizar proyecto: {e}")
        return False

def eliminar_proyecto(id_app):
    try:
        url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
        res = requests.delete(url, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al eliminar proyecto: {e}")
        return False