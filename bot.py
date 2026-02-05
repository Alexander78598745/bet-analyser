import requests
import json
import os
import time

# --- CONFIGURACIÓN PARA FOOTBALL-DATA.ORG ---
API_KEY = os.getenv('FOOTBALL_API_KEY')
HEADERS = {'X-Auth-Token': API_KEY}

# Ligas disponibles en el plan gratuito (Temporada Actual)
# PD = España, PL = Inglaterra, SA = Italia, BL1 = Alemania, FL1 = Francia
LIGAS = ['PD', 'PL', 'SA', 'BL1', 'FL1']

def actualizar_datos():
    stats_finales = {}
    print("⚽ Conectando con la base de datos 2025/2026...")

    for liga_code in LIGAS:
        url = f"https://api.football-data.org/v4/competitions/{liga_code}/standings"
        
        try:
            response = requests.get(url, headers=HEADERS)
            
            if response.status_code == 200:
                data = response.json()
                nombre_liga = data['competition']['name']
                # Buscamos la tabla general
                tabla = data['standings'][0]['table']
                
                print(f"✅ Procesando: {nombre_liga}")

                for equipo in tabla:
                    # Limpiamos el nombre para que sea más fácil de leer
                    nombre = equipo['team']['name'].replace("FC ", "").replace(" CD", "").strip()
                    
                    jugados = equipo['playedGames']
                    goles_favor = equipo['goalsFor']
                    goles_contra = equipo['goalsAgainst']
                    
                    if jugados > 0:
                        stats_finales[nombre] = {
                            "liga": nombre_liga,
                            "ga": round(goles_favor / jugados, 2),
                            "gc": round(goles_contra / jugados, 2)
                        }
            else:
                print(f"⚠️ Error {response.status_code} en liga {liga_code}")

            # IMPORTANTE: Esperamos 10 segundos entre ligas 
            # El plan gratuito solo permite 10 peticiones por minuto.
            time.sleep(10)

        except Exception as e:
            print(f"❌ Error en {liga_code}: {e}")

    # Guardamos el archivo JSON
    with open('equipos.json', 'w') as f:
        json.dump(stats_finales, f, indent=4)
    print("💾 ¡Base de datos de la temporada actual guardada!")

if __name__ == "__main__":
    actualizar_datos()
