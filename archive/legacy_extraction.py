import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

#Cargar claves de la API de eBay desde el archivo .env
current_path = Path(__file__).resolve()
env_path = current_path.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

EBAY_APP_ID = os.getenv("EBAY_APP_ID")

def buscar_productos(busqueda = "iphone 13"):
    print(f"Buscando {busqueda} en eBay España...")
          
    # URL de Sandbox (Pruebas)
    url = "https://svcs.ebay.com/services/search/FindingService/v1"

    #Parametros de la petición (headers y Payload)
    headers = {
        'X-EBAY-SOA-OPERATION-NAME': 'findItemsByKeywords',
        'X-EBAY-SOA-SECURITY-APPNAME': EBAY_APP_ID,
        'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'JSON',
        'X-EBAY-SOA-GLOBAL-ID': 'EBAY-ES' #Especificamos que queremos resultados de eBay España
    }

    params = {
        'keywords': busqueda,
        'paginationInput.entriesPerPage': 5, #Limitar a 5 resultados para pruebas
        'itemFilter(0).name': 'ListingType',
        'itemFilter(0).value': 'FixedPrice', #Solo productos con precio fijo
        'itemFilter(1).name': 'Condition',
        'itemFilter(1).value': 'New' #Solo productos nuevos
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        #verificamos si funcionó (Código 200 = OK)
        if response.status_code == 200:
            data= response.json()

            #Navegar por el JSON de eBay para llegar a los items
            items = data.get('findItemsByKeywordsResponse', [])[0] \
                        .get('searchResult', [])[0] \
                        .get('item', [])

            print(f"Encontrados {len(items)} productos para '{busqueda}'.")

            #Imprimir el primero para ver la estructura
            if items:
                primero = items[0]
                titulo = primero.get('title', [''])[0]
                precio = primero.get('sellingStatus', [])[0].get('currentPrice', [])[0].get('__value__')
                moneda = primero.get('sellingStatus', [])[0].get('currentPrice', [])[0].get('@currencyId')

                print(f"Ejemplo de producto encontrado:")
                print(f"Titulo: {titulo}")
                print(f"Precio: {precio} {moneda}")

                return items
        else:
            print(f"Error en la API: {response.status_code}")
            print(f"Mensaje: {response.text}")

    except Exception as e:
        print(f"Error al conectar con la API de eBay: {e}")
if __name__ == "__main__":
    #Prueba Rápida
    buscar_productos()