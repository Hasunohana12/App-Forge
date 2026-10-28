import os
import requests
import secrets
import string

PROJECT_REF = os.getenv('SUPABASE_URL', 'https://flyznurbkihesnylrwov.supabase.co').replace('https://', '').replace('.supabase.co', '')
API_KEY = os.getenv('SUPABASE_KEY', 'sb_publishable_E7bpFRnkfmdcV8ouIUEJrQ_tDUxF2sF')
BASE_URL = f"https://{PROJECT_REF}.supabase.co/rest/v1"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def obtener_clientes():
    try:
        response = requests.get(f"{BASE_URL}/cliente?select=*", headers=HEADERS)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []

def obtener_solicitudes_pendientes():
    try:
        url = f"{BASE_URL}/aplicacion?select=*"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            solicitudes = response.json()
            for sol in solicitudes:
                id_cli = sol.get('id_cliente')
                if id_cli:
                    res_cli = requests.get(f"{BASE_URL}/cliente?id_cliente=eq.{id_cli}", headers=HEADERS)
                    if res_cli.status_code == 200 and res_cli.json():
                        sol['cliente'] = res_cli.json()[0]
                    else:
                        sol['cliente'] = {'nombre': 'Cliente Desconocido', 'email': '-'}
                else:
                    sol['cliente'] = {'nombre': 'Contacto Directo', 'email': '-'}
            return solicitudes
            
        print(f"Error al obtener solicitudes ({response.status_code}): {response.text}")
        return []
    except Exception as e:
        print(f"Excepción en obtener_solicitudes_pendientes: {e}")
        return []

def obtener_aplicaciones():
    try:
        response = requests.get(f"{BASE_URL}/aplicacion?select=*", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Excepción en obtener_aplicaciones: {e}")
        return []

def generar_password_random(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def crear_solicitud_cliente(nombre, telefono, email, detalles_app):
    try:
        password_temp = generar_password_random()

        body_cliente = {
            "nombre": nombre,
            "email": email,
            "password": password_temp,
            "contacto": telefono or "-",
            "telefono": telefono or "-"
        }

        res_cliente = requests.post(f"{BASE_URL}/cliente", json=body_cliente, headers=HEADERS)
        
        id_cliente = None
        if res_cliente.status_code in (200, 201):
            data_cli = res_cliente.json()
            if isinstance(data_cli, list) and len(data_cli) > 0:
                id_cliente = data_cli[0].get("id_cliente")
            elif isinstance(data_cli, dict):
                id_cliente = data_cli.get("id_cliente")

        body_app = {
            "nombre": f"Solicitud: {nombre}",
            "descripcion": detalles_app or "Sin detalles especificados.",
            "estado": "PENDIENTE",
            "es_publico_portafolio": False
        }
        if id_cliente:
            body_app["id_cliente"] = id_cliente

        res_app = requests.post(f"{BASE_URL}/aplicacion", json=body_app, headers=HEADERS)
        
        if res_app.status_code in (200, 201):
            return {"exito": True, "password_temporal": password_temp}
            
        return {"exito": False, "password_temporal": None}
    except Exception as e:
        print(f"Excepción en crear_solicitud_cliente: {e}")
        return {"exito": False, "password_temporal": None}