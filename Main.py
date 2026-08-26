import requests

project_ref = "flyznurbkihesnylrwov"
api_key = "sb_publishable_E7bpFRnkfmdcV8ouIUEJrQ_tDUxF2sF"

url = f"https://{project_ref}.supabase.co/rest/v1/"

headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(url, headers=headers)
   
    if response.status_code in (200, 401):
        print("Conexión exitosa")
    else:
        print(f"Error en la conexión. Código: {response.status_code}")
       
except requests.exceptions.RequestException as e:
    print(f"Error al conectar: {e}")