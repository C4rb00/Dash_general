import pandas as pd

class MetricasInscritos:
    def __init__(self, df_inscritos: pd.DataFrame):
        self.df = df_inscritos.copy()
        self.metricas = []

    def _add_metric(self, categoria, subcategoria=None, valor=None, **kwargs):
        base = {
            "categoria": categoria,
            "subcategoria": subcategoria,
            "valor": valor
        }
        base.update(kwargs)
        self.metricas.append(base)

    def calcular_metricas_generales(self):
        self._add_metric("total_estudiantes", valor=len(self.df))
        self._add_metric("total_instituciones", valor=self.df['Nombre Institución'].nunique())
        self._add_metric("total_personal", valor=0)  

    def calcular_por_genero(self):
        genero_counts = self.df['Género'].value_counts()
        for genero, count in genero_counts.items():
            self._add_metric("genero", genero, count)

    def calcular_por_zona(self):
        zona_counts = self.df['Zona'].value_counts()
        for zona, count in zona_counts.items():
            self._add_metric("zona", zona, count)

    def calcular_por_tipo_deporte(self):
        tipo_counts = self.df['tipo deporte'].value_counts()
        for tipo, count in tipo_counts.items():
            self._add_metric("tipo_deporte", tipo, count)

    def calcular_por_zona_y_departamento(self):
        grouped = self.df.groupby(['Departamento Deportista', 'Zona']).size()
        for (dep, zona), count in grouped.items():
            self._add_metric("zona_depto", zona=zona, departamento=dep, valor=count)

    def calcular_por_deporte_y_tipo(self):
        grouped = self.df.groupby(['Deporte', 'tipo deporte']).size()
        for (dep, tipo), count in grouped.items():
            self._add_metric("deporte_tipo", deporte=dep, tipo=tipo, valor=count)

    def calcular_tendencia_por_fecha(self):
        self.df['fecha'] = pd.to_datetime(self.df['Fecha de Registro']).dt.date  # Solo la fecha
        tendencia = self.df.groupby('fecha').size()
        for fecha, count in tendencia.items():
            self._add_metric("tendencia", fecha=str(fecha), valor=count)

    def construir_metricas(self):
        self.calcular_metricas_generales()
        self.calcular_por_genero()
        self.calcular_por_zona()
        self.calcular_por_tipo_deporte()
        self.calcular_por_zona_y_departamento()
        self.calcular_por_deporte_y_tipo()
        self.calcular_tendencia_por_fecha()
        return pd.DataFrame(self.metricas)
