import os
import requests
import base64
import json
from dotenv import load_dotenv
from pathlib import Path

# Cargar Entorno
current_path = Path(__file__).resolve()
env_path = current_path.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.getenv("EBAY_APP_ID")
CLIENT_SECRET = os.getenv("EBAY_CERT_ID")

def obtener_token_oauth():
    """
    Intercambia tus credenciales por un Token de Acceso válido por 2 horas.
    """
    print("Solicitando Token OAuth 2.0...")
    
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    
    # eBay requiere que las credenciales vayan codificadas en Base64
    # Formato: Basic <Base64(CLIENT_ID:CLIENT_SECRET)>
    credenciales = f"{CLIENT_ID}:{CLIENT_SECRET}"
    credenciales_b64 = base64.b64encode(credenciales.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {credenciales_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # El body pide "client_credentials" y el alcance (scope) general
    payload = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        token = data["access_token"]
        print("✅ Token recibido correctamente.")
        return token
    else:
        print(f"❌ Error al obtener token: {response.status_code}")
        print(response.text)
        return None

def buscar_iphone_moderno(token):
    """
    Usa la Browse API (REST moderna) para buscar productos.
    """
    print("\nBuscando 'iPhone 13' con Browse API...")
    
    # URL MODERNA (Browse API)
    # Documentación: https://developer.ebay.com/api-docs/buy/browse/resources/item_summary/methods/search
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    
    headers = {
        "Authorization": f"Bearer {token}", # Aquí va el token que ganamos antes
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_ES" # Mercado España
    }
    
    params = {
        "q": "iPhone 13",
        "category_ids": "9355", # Categoría de Smartphones
        "limit": 5, # Solo 5 para probar
        "filter": "buyingOptions:{FIXED_PRICE},condition:{NEW}" # Filtros modernos
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # En la API moderna, los items están en 'itemSummaries'
        items = data.get("itemSummaries", [])
        print(f"📦 Encontrados {len(items)} productos.")
        
        for item in items:
            titulo = item.get("title")
            precio = item.get("price", {}).get("value")
            moneda = item.get("price", {}).get("currency")
            link = item.get("itemWebUrl")
            
            print(f"------------------------------------------------")
            print(f"📱 {titulo}")
            print(f"💰 {precio} {moneda}")
            print(f"🔗 {link}")
            
    else:
        print(f"❌ Error en la búsqueda: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # 1. Obtener la llave
    mi_token = obtener_token_oauth()
    
    # 2. Si hay llave, abrimos la puerta
    if mi_token:
        buscar_iphone_moderno(mi_token)