import os
import requests
import json

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

def crear_nuevo_proyecto(nombre, descripcion, estado="DISPONIBLE", fecha_inicio=None, es_publico=True, imagen_url=None, dev_lider_id=None, dev_ids=None, imagenes_paneles=None):
    body = {
        "nombre": nombre,
        "descripcion": descripcion,
        "estado": estado,
        "es_publico_portafolio": bool(es_publico)
    }
    if fecha_inicio:
        body["fecha_inicio"] = fecha_inicio
    if imagen_url:
        body["imagen_url"] = imagen_url
    if imagenes_paneles:
        body["imagenes_paneles"] = json.dumps(imagenes_paneles) if isinstance(imagenes_paneles, list) else imagenes_paneles

    try:
        res = requests.post(f"{BASE_URL}/aplicacion", json=body, headers=HEADERS)
        if res.status_code not in (200, 201):
            print(f"Error POST Supabase ({res.status_code}): {res.text}")
            return None
        
        data = res.json()
        proyecto_creado = data[0] if isinstance(data, list) and data else data
        id_app = proyecto_creado.get('id_app')

        if id_app:
            if dev_lider_id:
                body_lider = {
                    "id_app": int(id_app),
                    "id_desarrollador": int(dev_lider_id),
                    "rol_desempenado": "LIDER"
                }
                requests.post(f"{BASE_URL}/desarrollador_aplicacion", json=body_lider, headers=HEADERS)

            if dev_ids:
                for dev_id in dev_ids:
                    if str(dev_id) != str(dev_lider_id):
                        body_rel = {
                            "id_app": int(id_app),
                            "id_desarrollador": int(dev_id),
                            "rol_desempenado": "DESARROLLADOR"
                        }
                        requests.post(f"{BASE_URL}/desarrollador_aplicacion", json=body_rel, headers=HEADERS)

        return proyecto_creado
    except Exception as e:
        print(f"Excepción en crear_nuevo_proyecto: {e}")
        return None

def actualizar_proyecto(id_app, nombre, descripcion, estado, fecha_inicio=None, imagen_url=None, es_publico=True, dev_lider_id=None, dev_ids=None, imagenes_paneles=None, eliminar_panel=None):
    url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
    
    proyecto_actual = obtener_proyecto_por_id(id_app)
    paneles_existentes = []
    if proyecto_actual and proyecto_actual.get('imagenes_paneles'):
        try:
            p_val = proyecto_actual['imagenes_paneles']
            paneles_existentes = json.loads(p_val) if isinstance(p_val, str) else p_val
        except Exception:
            paneles_existentes = []

    if eliminar_panel and eliminar_panel in paneles_existentes:
        paneles_existentes.remove(eliminar_panel)

    if imagenes_paneles and isinstance(imagenes_paneles, list):
        for img_p in imagenes_paneles:
            if img_p not in paneles_existentes:
                paneles_existentes.append(img_p)

    body = {
        "nombre": nombre,
        "descripcion": descripcion,
        "estado": estado,
        "es_publico_portafolio": bool(es_publico),
        "imagenes_paneles": json.dumps(paneles_existentes)
    }
    if fecha_inicio:
        body["fecha_inicio"] = fecha_inicio
    if imagen_url:
        body["imagen_url"] = imagen_url

    try:
        res = requests.patch(url, json=body, headers=HEADERS)

        requests.delete(f"{BASE_URL}/desarrollador_aplicacion?id_app=eq.{id_app}", headers=HEADERS)
        
        if dev_lider_id:
            body_lider = {
                "id_app": int(id_app),
                "id_desarrollador": int(dev_lider_id),
                "rol_desempenado": "LIDER"
            }
            requests.post(f"{BASE_URL}/desarrollador_aplicacion", json=body_lider, headers=HEADERS)

        if dev_ids:
            for dev_id in dev_ids:
                if str(dev_id) != str(dev_lider_id):
                    body_rel = {
                        "id_app": int(id_app),
                        "id_desarrollador": int(dev_id),
                        "rol_desempenado": "DESARROLLADOR"
                    }
                    requests.post(f"{BASE_URL}/desarrollador_aplicacion", json=body_rel, headers=HEADERS)

        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al actualizar proyecto: {e}")
        return False

def eliminar_proyecto(id_app):
    try:
        requests.delete(f"{BASE_URL}/desarrollador_aplicacion?id_app=eq.{id_app}", headers=HEADERS)
        url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
        res = requests.delete(url, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al eliminar proyecto: {e}")
        return False