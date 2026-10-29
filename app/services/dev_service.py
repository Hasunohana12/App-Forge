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
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error en obtener_desarrolladores: {e}")
        return []

def asignar_dev_a_proyecto(id_app, id_dev, rol="DESARROLLADOR", horas_estimadas_dia=None):
    try:
        body_rel = {
            "id_app": int(id_app),
            "id_desarrollador": int(id_dev),
            "rol_desempenado": rol or "DESARROLLADOR"
        }
        if horas_estimadas_dia:
            body_rel["horas_estimadas_dia"] = int(horas_estimadas_dia)

        res = requests.post(f"{BASE_URL}/desarrollador_aplicacion", json=body_rel, headers=HEADERS)

        body_app = {"estado_atencion": "ASIGNADO"}
        requests.patch(f"{BASE_URL}/aplicacion?id_app=eq.{id_app}", json=body_app, headers=HEADERS)

        return res.status_code in (200, 201)
    except Exception as e:
        print(f"Error al asignar dev a proyecto: {e}")
        return False

def obtener_proyectos_por_dev(id_desarrollador):
    try:
        url = f"{BASE_URL}/desarrollador_aplicacion?id_desarrollador=eq.{id_desarrollador}&select=rol_desempenado,horas_estimadas_dia,aplicacion(*)"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            relaciones = response.json()
            proyectos = []
            for rel in relaciones:
                app_data = rel.get('aplicacion')
                if app_data:
                    app_data['rol_asignado'] = rel.get('rol_desempenado', 'DESARROLLADOR')
                    app_data['horas_dedicadas'] = rel.get('horas_estimadas_dia', 4)
                    proyectos.append(app_data)
            return proyectos
        return []
    except Exception as e:
        print(f"Error al obtener proyectos por dev: {e}")
        return []

def cambiar_estado_disponibilidad(id_dev, esta_disponible):
    try:
        url = f"{BASE_URL}/desarrollador?id_desarrollador=eq.{id_dev}"
        body = {"disponible": bool(esta_disponible)}
        res = requests.patch(url, json=body, headers=HEADERS)
        return res.status_code in (200, 204)
    except Exception as e:
        print(f"Error al cambiar disponibilidad: {e}")
        return False

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

def actualizar_desarrollador(id_dev, nombre, especialidad, email, contrasena=None):
    url = f"{BASE_URL}/desarrollador?id_desarrollador=eq.{id_dev}"
    body = {
        "nombre_completo": nombre,
        "especialidad": especialidad,
        "email": email
    }
    if contrasena:
        body["contrasena"] = contrasena

    try:
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