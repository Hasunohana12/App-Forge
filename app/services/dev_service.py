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

def obtener_desarrolladores():
    response = requests.get(f"{BASE_URL}/desarrollador?select=*", headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def asignar_dev_a_proyecto(id_app, id_desarrollador, rol, horas):
    body = {
        "id_app": id_app,
        "id_desarrollador": id_desarrollador,
        "rol": rol,
        "horas_dedicadas": horas
    }
    requests.post(f"{BASE_URL}/desarrolladorpordetalle", json=body, headers=HEADERS)
    
    patch_url = f"{BASE_URL}/aplicacion?id_app=eq.{id_app}"
    requests.patch(patch_url, json={"estado": "ASIGNADO"}, headers=HEADERS)

def obtener_proyectos_por_dev(id_desarrollador):
    url = f"{BASE_URL}/desarrolladorpordetalle?select=rol,horas_dedicadas,aplicacion(nombre,estado)&id_desarrollador=eq.{id_desarrollador}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def crear_nuevo_desarrollador(nombre_completo, especialidad, email, contrasena):
    body = {
        "nombre_completo": nombre_completo,
        "especialidad": especialidad,
        "email": email,
        "contrasena": contrasena
    }
    response = requests.post(f"{BASE_URL}/desarrollador", json=body, headers=HEADERS)
    return response.json() if response.status_code in (200, 201) else None

def obtener_desarrollador_por_credenciales(email, password):
    url = f"{BASE_URL}/desarrollador?email=eq.{email}&contrasena=eq.{password}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        datos = response.json()
        return datos[0] if datos else None
    return None