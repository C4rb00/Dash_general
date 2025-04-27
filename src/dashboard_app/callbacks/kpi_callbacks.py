from dash import callback, Output, Input, dcc, callback_context
import pandas as pd
import plotly.graph_objects as go
from layout.components import DashboardCard
from transformers.kpi_metrics import MetricasInscritos
from dash import html
from config import TIPOS_DEPORTE, COLOR_MAP

# Variable global para almacenar los datos
data = None

def init_callbacks(app, initial_data):
    global data
    data = initial_data['data']

    @callback(
        Output("filtered-data-store", "data"),
        Input("filtrar-btn", "n_clicks"),
        Input("departamento-dropdown", "value"),
        Input("municipio-dropdown", "value"),
        prevent_initial_call=True
    )
    def filtrar_datos(n_clicks, departamentos_seleccionados, municipios_seleccionados):
        df_filtrado = data
        if departamentos_seleccionados:
            df_filtrado = df_filtrado[df_filtrado["Departamento Deportista"].isin(departamentos_seleccionados)]
        if municipios_seleccionados:
            df_filtrado = df_filtrado[df_filtrado["Municipio Deportista"].isin(municipios_seleccionados)]
        return df_filtrado.to_dict("records")

    @callback(
        Output("card-total-estudiantes", "children"),
        Output("card-total-instituciones", "children"),
        Output("card-total-personal", "children"),
        Input("filtered-data-store", "data")
    )
    def actualizar_metricas(datos_filtrados):
        df = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        metricas = MetricasInscritos(df)
        df_metricas = metricas.construir_metricas()
        total_estudiantes = int(df_metricas[df_metricas["categoria"] == "total_estudiantes"]["valor"].values[0])
        total_instituciones = int(df_metricas[df_metricas["categoria"] == "total_instituciones"]["valor"].values[0])
        total_personal = int(df_metricas[df_metricas["categoria"] == "total_personal"]["valor"].values[0])
        return (
            DashboardCard(
                card_type="metric",
                icon_path="/assets/Images/Imagen1.png",
                value=f"{total_estudiantes:,}",
                title_lines=["Total de estudiantes", "inscritos"],
                border_color="#293377"
            ).render(),
            DashboardCard(
                card_type="metric",
                icon_path="/assets/Images/Imagen2.png",
                value=f"{total_instituciones:,}",
                title_lines=["Total de instituciones", "inscritas"],
                border_color="#FFA354"
            ).render(),
            DashboardCard(
                card_type="metric",
                icon_path="/assets/Images/Imagen1.png",
                value=f"{total_personal:,}",
                title_lines=["Total de personal de", "apoyo inscrito"],
                border_color="#602A8C"
            ).render()
        )

    @callback(
        Output("trendline-card", "children"),
        Input("filtered-data-store", "data")
    )
    def actualizar_trendline(datos_filtrados):
        df = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        trend_data = df.copy()
        trend_data['Fecha'] = pd.to_datetime(trend_data['Fecha de Registro']).dt.date
        trend_data = trend_data.groupby('Fecha').size().reset_index(name='inscritos')
        return DashboardCard(
            card_type="trendline",
            x_data=trend_data['Fecha'],
            y_data=trend_data['inscritos'],
            trend_title="Tendencia de inscripciones"
        ).render()

    @callback(
        Output("gender-card", "children"),
        Input("filtered-data-store", "data")
    )
    def actualizar_gender(datos_filtrados):
        df = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        male = int(df[df['Género'] == 'Hombre'].shape[0])
        female = int(df[df['Género'] == 'Mujer'].shape[0])
        return DashboardCard(
            card_type="gender",
            image_path="/assets/Images/img_gender.png",
            male_value=male,
            female_value=female
        ).render()

    @callback(
        Output("zona-donut-card", "children"),
        Input("filtered-data-store", "data")
    )
    def actualizar_zona_donut(datos_filtrados):
        df = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        zona_counts = df['Zona'].value_counts()
        zona_labels = zona_counts.index.tolist()
        zona_values = zona_counts.values.tolist()
        return DashboardCard(
            card_type="donut",
            labels=zona_labels,
            values=zona_values,
            colors=["#FFA354", "#E5C473"],
            donut_title="Distribución por Zona"
        ).render()

    @callback(
        Output("tipo-donut-card", "children"),
        Input("filtered-data-store", "data")
    )
    def actualizar_tipo_donut(datos_filtrados):
        df = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        tipo_counts = df['tipo deporte'].value_counts()
        tipo_labels = tipo_counts.index.tolist()
        tipo_values = tipo_counts.values.tolist()
        colors = [COLOR_MAP[tipo] for tipo in tipo_labels]
        return DashboardCard(
            card_type="donut",
            labels=tipo_labels,
            values=tipo_values,
            colors=colors,
            donut_title="Tipo de Deporte"
        ).render()

    @callback(
        Output("bar-estudiantes-card", "children"),
        Input("filtered-data-store", "data")
    )
    def actualizar_bar_estudiantes(datos_filtrados):
        df = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        
        # Obtener los datos necesarios
        departamentos = sorted(df['Departamento Deportista'].dropna().unique().tolist())
        rural_counts = df[df['Zona'].str.lower() == 'rural']['Departamento Deportista'].value_counts()
        urbano_counts = df[df['Zona'].str.lower() == 'urbano']['Departamento Deportista'].value_counts()
        rural = [rural_counts.get(dep, 0) for dep in departamentos]
        urbano = [urbano_counts.get(dep, 0) for dep in departamentos]
        
        # Crear el gráfico usando DashboardCard
        return DashboardCard(
            card_type="bar",
            x_data=departamentos,
            y_data=[rural, urbano],
            trend_title="Estudiantes inscritos por departamento"
        ).render()

    @callback(
        Output("grafico-deportes-individuales", "figure"),
        Input("tipo-deporte-checklist", "value"),
        Input("filtered-data-store", "data")
    )
    def actualizar_dashboard(tipos_seleccionados, datos_filtrados):
        df_filtrado = pd.DataFrame(datos_filtrados) if datos_filtrados else data
        deportes_data = df_filtrado[df_filtrado["tipo deporte"].isin(tipos_seleccionados)]
        deportes_group = deportes_data.groupby(['Deporte', 'tipo deporte']).size().reset_index(name='total')
        deportes_unicos = sorted(deportes_group['Deporte'].unique())
        barras = []
        for tipo in tipos_seleccionados:
            y = []
            for deporte in deportes_unicos:
                row = deportes_group[(deportes_group['Deporte'] == deporte) & (deportes_group['tipo deporte'] == tipo)]
                y.append(int(row['total'].values[0]) if not row.empty else 0)
            barras.append(go.Bar(x=deportes_unicos, y=y, name=tipo.title(), marker_color=COLOR_MAP.get(tipo, "#888888")))
        deportes_fig = go.Figure(data=barras)
        deportes_fig.update_layout(barmode="group")
        return deportes_fig

    @callback(
        Output("municipio-dropdown", "options"),
        Input("departamento-dropdown", "value")
    )
    def actualizar_municipios(departamentos_seleccionados):
        if not departamentos_seleccionados:
            municipios_filtrados = data['Municipio Deportista'].dropna().unique()
        else:
            municipios_filtrados = data[data['Departamento Deportista'].isin(departamentos_seleccionados)]['Municipio Deportista'].dropna().unique()
        return [{"label": mun, "value": mun} for mun in sorted(municipios_filtrados)]

    @callback(
        Output("tipo-deporte-checklist", "value"),
        [Input("conjunto-legend", "n_clicks"),
         Input("individual-legend", "n_clicks"),
         Input("paradeporte-legend", "n_clicks")],
        [Input("tipo-deporte-checklist", "value")]
    )
    def toggle_tipo_deporte(conjunto_clicks, individual_clicks, paradeporte_clicks, current_values):
        if not current_values:
            return TIPOS_DEPORTE
            
        triggered = callback_context.triggered
        if not triggered:
            return current_values

        button_id = triggered[0]["prop_id"].split(".")[0]
        tipo_map = {
            "conjunto-legend": "conjunto",
            "individual-legend": "individual",
            "paradeporte-legend": "para deporte"
        }
        
        if button_id in tipo_map:
            tipo = tipo_map[button_id]
            if tipo in current_values:
                return [v for v in current_values if v != tipo]
            else:
                return current_values + [tipo]
        
        return current_values

    @callback(
        [Output("conjunto-legend", "style"),
         Output("individual-legend", "style"),
         Output("paradeporte-legend", "style")],
        [Input("tipo-deporte-checklist", "value")]
    )
    def update_legend_styles(selected_tipos):
        styles = []
        for tipo in ["conjunto", "individual", "para deporte"]:
            if tipo in selected_tipos:
                styles.append({"opacity": 1.0})
            else:
                styles.append({"opacity": 0.5})
        return styles