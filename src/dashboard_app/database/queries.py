import pandas as pd
from transformers.kpi_metrics import MetricasInscritos

class QueriesInscripciones:
    @staticmethod
    def get_inscripciones_data(file_path: str) -> pd.DataFrame:
        data = pd.read_excel(file_path)
        data['tipo deporte'] = data['tipo deporte'].str.strip().str.lower()
        return data

    @staticmethod
    def get_metricas(data: pd.DataFrame):
        metricas = MetricasInscritos(data)
        return metricas.construir_metricas()

    @staticmethod
    def get_zona_counts(data: pd.DataFrame):
        zona_counts = data['Zona'].value_counts()
        return zona_counts.index.tolist(), zona_counts.values.tolist()

    @staticmethod
    def get_tipo_counts(data: pd.DataFrame):
        tipo_counts = data['tipo deporte'].value_counts()
        return tipo_counts.index.tolist(), tipo_counts.values.tolist()

    @staticmethod
    def get_departamentos(data: pd.DataFrame):
        return sorted(data['Departamento Deportista'].dropna().unique().tolist())

    @staticmethod
    def get_municipios(data: pd.DataFrame):
        return sorted(data['Municipio Deportista'].dropna().unique().tolist())

    @staticmethod
    def get_rural_urbano_counts(data: pd.DataFrame, departamentos):
        rural_counts = data[data['Zona'].str.lower() == 'rural']['Departamento Deportista'].value_counts()
        urbano_counts = data[data['Zona'].str.lower() == 'urbano']['Departamento Deportista'].value_counts()
        rural = [rural_counts.get(dep, 0) for dep in departamentos]
        urbano = [urbano_counts.get(dep, 0) for dep in departamentos]
        return rural, urbano

    @staticmethod
    def get_trend_data(data: pd.DataFrame):
        trend_data = data.copy()
        trend_data['Fecha'] = pd.to_datetime(trend_data['Fecha de Registro']).dt.date
        return trend_data.groupby('Fecha').size().reset_index(name='inscritos')

    @staticmethod
    def get_deportes_data(data: pd.DataFrame):
        return data.groupby(['Deporte', 'tipo deporte']).size().reset_index(name='total')
