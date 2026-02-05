import requests
import json
import os

API_KEY = os.getenv('FOOTBALL_API_KEY') 
HEADERS = {'x-apisports-key': API_KEY}

# Probamos solo con LaLiga (140) para no gastar intentos
LIGAS = [140] 
TEMPORADA = 2025 

def actualizar_datos():
    stats_finales = {}
    print(f"DEBUG: Usando API Key: {API_KEY[:5]}***") # Solo muestra el inicio por seguridad

    for liga_id in LIGAS:
        url = f"https://v3.football.api-sports.io/standings?league={liga_id}&season={TEMPORADA}"
        print(f"DEBUG: Llamando a URL: {url}")
        
        try:
            response = requests.get(url, headers=HEADERS)
            data = response.json()
            
            # ESTO NOS DIRÁ EL ERROR REAL
            print(f"DEBUG: Respuesta de la API: {data}")

            if not data.get('response'):
                print(f"⚠️ Error detallado de la API: {data.get('errors')}")
                continue

            datos_liga = data['response'][0]['league']
            nombre_liga = datos_liga['name']
            tabla = datos_liga['standings'][0]

            for equipo in tabla:
                nombre = equipo['team']['name']
                stats = equipo['all']
                jugados = stats['played']
                if jugados > 0:
                    stats_finales[nombre] = {
                        "liga": nombre_liga,
                        "ga": round(stats['goals']['for'] / jugados, 2),
                        "gc": round(stats['goals']['against'] / jugados, 2)
                    }
                    
        except Exception as e:
            print(f"❌ Error crítico: {e}")

    with open('equipos.json', 'w') as f:
        json.dump(stats_finales, f, indent=4)
    print("💾 Archivo guardado.")

if __name__ == "__main__":
    actualizar_datos()
