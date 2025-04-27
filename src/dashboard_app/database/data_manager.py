import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, date
from .queries import QueriesInscripciones as Queries
from config import DATA_FILE, CACHE_FILE

class DataManager:
    @staticmethod
    def _convert_numpy_types(obj):
        """Convierte tipos de numpy y otros tipos complejos a tipos Python nativos"""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: DataManager._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [DataManager._convert_numpy_types(item) for item in obj]
        return obj

    @staticmethod
    def _prepare_data_for_cache(data):
        """Prepara los datos para ser guardados en caché, asegurando que sean serializables"""
        if isinstance(data, pd.DataFrame):
            # Convertir columnas de fecha a string en formato ISO
            for col in data.columns:
                if pd.api.types.is_datetime64_any_dtype(data[col]):
                    data[col] = data[col].dt.strftime('%Y-%m-%d')
                elif isinstance(data[col].iloc[0], (datetime, date)) if len(data) > 0 else False:
                    data[col] = data[col].apply(lambda x: x.isoformat() if isinstance(x, (datetime, date)) else x)
            return DataManager._convert_numpy_types(data)
        elif isinstance(data, dict):
            return {key: DataManager._prepare_data_for_cache(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [DataManager._prepare_data_for_cache(item) for item in data]
        elif isinstance(data, (datetime, date)):
            return data.isoformat()
        return DataManager._convert_numpy_types(data)

    @staticmethod
    def _save_to_cache(data):
        """Guarda los datos procesados en el cache"""
        try:
            os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
            cache_data = {
                'last_update': datetime.now().isoformat(),
                'data': DataManager._prepare_data_for_cache(data)
            }
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print("Datos guardados en cache correctamente")
        except Exception as e:
            print(f"Error al guardar en cache: {str(e)}")
            raise

    @staticmethod
    def _load_from_cache():
        """Carga los datos desde el cache"""
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                data = cache_data['data']
                
                # Convertir datos de vuelta a DataFrames donde sea necesario
                if 'data' in data and isinstance(data['data'], list):
                    df = pd.DataFrame(data['data'])
                    # Convertir columnas de fecha de vuelta a datetime
                    date_columns = [col for col in df.columns if isinstance(df[col].iloc[0], str) and 
                                  df[col].iloc[0].count('-') == 2]
                    for col in date_columns:
                        try:
                            df[col] = pd.to_datetime(df[col])
                        except:
                            pass  # Si la conversión falla, mantener como string
                    data['data'] = df
                
                print("Datos cargados desde cache correctamente")
                return data
        except Exception as e:
            print(f"Error al cargar desde cache: {str(e)}")
            return None

    @staticmethod
    def _should_update_cache():
        """Verifica si se debe actualizar el caché"""
        try:
            # Si el archivo de caché no existe
            if not os.path.exists(CACHE_FILE):
                return True
            
            # Si el archivo Excel es más reciente que el caché
            excel_modified = os.path.getmtime(DATA_FILE)
            cache_modified = os.path.getmtime(CACHE_FILE)
            return excel_modified > cache_modified
        except:
            return True

    @staticmethod
    def initialize_data():
        """Inicializa los datos, usando caché si está disponible"""
        # Verificar si podemos usar el caché
        if not DataManager._should_update_cache():
            cached_data = DataManager._load_from_cache()
            if cached_data is not None:
                print("Usando datos en caché...")
                return cached_data

        print("Procesando datos desde Excel...")
        # Cargar datos iniciales
        data = Queries.get_inscripciones_data(DATA_FILE)
        
        # Obtener métricas
        df_metricas = Queries.get_metricas(data)
        total_estudiantes = int(df_metricas[df_metricas["categoria"] == "total_estudiantes"]["valor"].values[0])
        total_instituciones = int(df_metricas[df_metricas["categoria"] == "total_instituciones"]["valor"].values[0])
        total_personal = int(df_metricas[df_metricas["categoria"] == "total_personal"]["valor"].values[0])

        # Obtener datos para gráficos
        zona_labels, zona_values = Queries.get_zona_counts(data)
        tipo_labels, tipo_values = Queries.get_tipo_counts(data)
        departamentos = Queries.get_departamentos(data)
        municipios = Queries.get_municipios(data)
        rural, urbano = Queries.get_rural_urbano_counts(data, departamentos)
        trend_data = Queries.get_trend_data(data)
        deportes_data = Queries.get_deportes_data(data)
        
        processed_data = {
            'data': data,
            'metricas': {
                'total_estudiantes': total_estudiantes,
                'total_instituciones': total_instituciones,
                'total_personal': total_personal
            },
            'zona': {
                'labels': zona_labels,
                'values': zona_values
            },
            'tipo': {
                'labels': tipo_labels,
                'values': tipo_values
            },
            'ubicacion': {
                'departamentos': departamentos,
                'municipios': municipios,
                'rural': rural,
                'urbano': urbano
            },
            'trend_data': trend_data,
            'deportes_data': deportes_data
        }

        print("\n=== DATOS PROCESADOS ===")
        print("\nMétricas:")
        print(f"Total Estudiantes: {total_estudiantes}")
        print(f"Total Instituciones: {total_instituciones}")
        print(f"Total Personal: {total_personal}")
        
        print("\nDatos por Zona:")
        for label, value in zip(zona_labels, zona_values):
            print(f"{label}: {value}")
            
        print("\nDatos por Tipo:")
        for label, value in zip(tipo_labels, tipo_values):
            print(f"{label}: {value}")
            
        print("\nDatos de Tendencia:")
        print(trend_data)
            
        print("\nDatos de Deportes:")
        print(deportes_data)
        
        print("\nDatos por Ubicación:")
        print(f"Departamentos: {departamentos}")
        print(f"Rural vs Urbano:")
        for dep, (r, u) in zip(departamentos, zip(rural, urbano)):
            print(f"{dep}: Rural={r}, Urbano={u}")
        
        print("\n=====================")

        # Guardar en caché
        DataManager._save_to_cache(processed_data)
        
        return processed_data 