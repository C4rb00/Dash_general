import dash
import dash_bootstrap_components as dbc
from database.data_manager import DataManager
from layout.layout import get_layout
from config import TIPOS_DEPORTE
from callbacks.kpi_callbacks import init_callbacks

def create_app():
    # Inicializar datos
    initial_data = DataManager.initialize_data()
    
    # Crear aplicación Dash
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    # Configurar layout
    app.layout = get_layout(
        departamentos=initial_data['ubicacion']['departamentos'],
        municipios=initial_data['ubicacion']['municipios'],
        TIPOS_DEPORTE=TIPOS_DEPORTE
    )
    
    # Inicializar callbacks
    init_callbacks(app, initial_data)
    
    return app, initial_data 