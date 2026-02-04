import requests
import json
import os

# --- CONFIGURACIÓN ---
# La API Key se toma de los Secretos de GitHub
API_KEY = os.getenv('FOOTBALL_API_KEY') 
HEADERS = {'x-apisports-key': API_KEY}

# IDs Ligas: 140=LaLiga, 39=Premier, 135=Serie A, 78=Bundesliga, 61=Ligue 1, 2=Champions
LIGAS = [140, 39, 135, 78, 61, 2] 
TEMPORADA = 2025 # Temporada actual (2025-2026)

def actualizar_datos():
    stats_finales = {}
    print("⚽ Iniciando escaneo de ligas...")

    for liga_id in LIGAS:
        # Usamos 'standings' para descargar toda la liga en 1 sola petición
        url = f"https://v3.football.api-sports.io/standings?league={liga_id}&season={TEMPORADA}"
        
        try:
            response = requests.get(url, headers=HEADERS).json()
            
            if not response.get('response'):
                print(f"⚠️ Sin datos para liga {liga_id}. Revisa API Key o Temporada.")
                continue

            datos_liga = response['response'][0]['league']
            nombre_liga = datos_liga['name']
            tabla = datos_liga['standings'][0]

            print(f"✅ Descargando: {nombre_liga}")

            for equipo in tabla:
                nombre = equipo['team']['name']
                stats = equipo['all']
                jugados = stats['played']
                
                # Solo procesamos si han jugado al menos un partido
                if jugados > 0:
                    stats_finales[nombre] = {
                        "liga": nombre_liga,
                        "ga": round(stats['goals']['for'] / jugados, 2),    # Goles a Favor Promedio
                        "gc": round(stats['goals']['against'] / jugados, 2) # Goles en Contra Promedio
                    }
                    
        except Exception as e:
            print(f"❌ Error en liga {liga_id}: {e}")

    # Guardamos el archivo JSON
    with open('equipos.json', 'w') as f:
        json.dump(stats_finales, f, indent=4)
    print("💾 Base de datos 'equipos.json' actualizada.")

if __name__ == "__main__":
    actualizar_datos()
