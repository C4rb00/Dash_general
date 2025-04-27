import os

# Configuración de colores
COLOR_MAP = {
    "conjunto": "#001F54",    # Azul oscuro
    "individual": "#AAB8D8",  # Gris azulado
    "para deporte": "#5167F1" # Azul brillante
}

# Tipos de deporte
TIPOS_DEPORTE = ["conjunto", "individual", "para deporte"]

# Rutas
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(CURRENT_DIR, "database", "inscripciones.xlsx")
CACHE_FILE = os.path.join(CURRENT_DIR, "database", "data_cache.json")
