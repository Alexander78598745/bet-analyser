import requests
import json
import os

# --- CONFIGURACIÓN ---
API_KEY = os.getenv('FOOTBALL_API_KEY') 
HEADERS = {'x-apisports-key': API_KEY}

# IDs: 140=LaLiga, 39=Premier, 135=Serie A, 78=Bundesliga, 61=Ligue 1
LIGAS = [140, 39, 135, 78, 61] 

# CAMBIO IMPORTANTE: Usamos 2024 porque el plan gratis bloquea la 2025
TEMPORADA = 2024 

def actualizar_datos():
    stats_finales = {}
    print(f"⚽ Iniciando escaneo de temporada {TEMPORADA}...")

    for liga_id in LIGAS:
        url = f"https://v3.football.api-sports.io/standings?league={liga_id}&season={TEMPORADA}"
        
        try:
            response = requests.get(url, headers=HEADERS).json()
            
            # Si hay error de plan, lo saltamos sin romper el programa
            if response.get('errors'):
                print(f"⚠️ Aviso en liga {liga_id}: {response.get('errors')}")
                continue

            if not response.get('response'):
                print(f"⚠️ Sin datos para liga {liga_id}.")
                continue

            datos_liga = response['response'][0]['league']
            nombre_liga = datos_liga['name']
            tabla = datos_liga['standings'][0]

            print(f"✅ Descargando: {nombre_liga}")

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
            print(f"❌ Error en liga {liga_id}: {e}")

    # Guardamos el archivo JSON
    with open('equipos.json', 'w') as f:
        json.dump(stats_finales, f, indent=4)
    print("💾 Base de datos 'equipos.json' guardada con éxito.")

if __name__ == "__main__":
    actualizar_datos()
