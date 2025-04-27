from dash import dcc, html
import dash_bootstrap_components as dbc
from layout.components import DashboardCard



def get_layout(departamentos, municipios, TIPOS_DEPORTE):
    return html.Div(className="app-container", children=[
        dcc.Store(id="filtered-data-store"),
        dbc.Container([
            # Sección de filtros
            html.H4("General", className="mt-4 mb-3 dash-card-title"),
            dbc.Row([
                dbc.Col(
                    html.Label("Filtrar por departamento:", className="departamento-label"),
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="departamento-dropdown",
                        options=[{"label": dep, "value": dep} for dep in departamentos],
                        multi=True,
                        placeholder="Seleccionar departamento",
                        className="departamento-dropdown"
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="municipio-dropdown",
                        options=[{"label": mun, "value": mun} for mun in municipios],
                        multi=True,
                        placeholder="Seleccionar municipio",
                        className="municipio-dropdown"
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Seleccionar institución",
                        disabled=True,
                        className="institucion-dropdown"
                    ),
                    width=3
                ),
                dbc.Col(
                    html.Button("Filtrar", id="filtrar-btn", className="w-100 filter-btn"),
                    width=1
                ),
            ], className="mb-4", align="end"),

            # Métricas y gráficos
            dbc.Row([
                dbc.Col(
                    DashboardCard(
                        card_type="metric",
                        icon_path="/assets/Images/Imagen1.png",
                        value="0",
                        title_lines=["Total de estudiantes", "inscritos"],
                        border_color="#293377"
                    ).render(),
                    id="card-total-estudiantes",
                    width=4,
                    className="h-300"
                ),
                dbc.Col(
                    DashboardCard(
                        card_type="metric",
                        icon_path="/assets/Images/Imagen2.png",
                        value="0",
                        title_lines=["Total de instituciones", "inscritas"],
                        border_color="#FFA354"
                    ).render(),
                    id="card-total-instituciones",
                    width=4,
                    className="h-300"
                ),
                dbc.Col(
                    DashboardCard(
                        card_type="metric",
                        icon_path="/assets/Images/Imagen1.png",
                        value="0",
                        title_lines=["Total de personal de", "apoyo inscrito"],
                        border_color="#602A8C"
                    ).render(),
                    id="card-total-personal",
                    width=4,
                    className="h-300"
                )
            ], className="mb-4 align-items-stretch"),

            dbc.Row([
                dbc.Col(
                    DashboardCard(
                        card_type="trendline",
                        x_data=[],
                        y_data=[],
                        trend_title=""
                    ).render(),
                    id="trendline-card",
                    width=8,
                    className="h-454"
                ),
                dbc.Col(
                    DashboardCard(
                        card_type="gender",
                        image_path="/assets/Images/img_gender.png",
                        male_value=0,
                        female_value=0
                    ).render(),
                    id="gender-card",
                    width=4,
                    className="h-454"
                )
            ], className="mb-4 align-items-stretch"),

            dbc.Row([
                dbc.Col(
                    DashboardCard(
                        card_type="donut",
                        labels=[],
                        values=[],
                        colors=["#FFA354", "#E5C473"],
                        donut_title="Distribución por Zona"
                    ).render(),
                    id="zona-donut-card",
                    width=6,
                    className="h-454"
                ),
                dbc.Col(
                    DashboardCard(
                        card_type="donut",
                        labels=[],
                        values=[],
                        colors=["#5167F1", "#AAB8D8", "#001F54"],
                        donut_title="Tipo de Deporte"
                    ).render(),
                    id="tipo-donut-card",
                    width=6,
                    className="h-454"
                ),
            ], className="mb-4 align-items-stretch"),

            dbc.Row([
                dbc.Col(
                    DashboardCard(
                        card_type="bar",
                        x_data=departamentos,
                        y_data=[[0] * len(departamentos), [0] * len(departamentos)],
                        trend_title="Estudiantes inscritos por departamento"
                    ).render(),
                    id="bar-estudiantes-card",
                    width=6,
                    className="h-454"
                ),
                dbc.Col(
                    html.Div([
                        html.H5("Inscritos por deporte", className="dash-card-title"),
                        html.Div(className="dash-card-divider"),
                        # Checklist oculto para los callbacks
                        dcc.Checklist(
                            id="tipo-deporte-checklist",
                            options=[{"label": tipo.title(), "value": tipo} for tipo in TIPOS_DEPORTE],
                            value=TIPOS_DEPORTE,
                            style={'display': 'none'}
                        ),
                        # Leyenda visual
                        html.Div([
                            html.Span([
                                html.Span(className="legend-color", style={"backgroundColor": "#001F54"}),
                                "Conjunto"
                            ], className="gender-legend-item", id="conjunto-legend"),
                            html.Span([
                                html.Span(className="legend-color", style={"backgroundColor": "#AAB8D8"}),
                                "Individual"
                            ], className="gender-legend-item", id="individual-legend"),
                            html.Span([
                                html.Span(className="legend-color", style={"backgroundColor": "#5167F1"}),
                                "Para deporte"
                            ], className="gender-legend-item", id="paradeporte-legend")
                        ], className="gender-legend"),
                        dcc.Graph(
                            id="grafico-deportes-individuales",
                            className="dash-graph"
                        )
                    ], className="dash-card"),
                    width=6,
                    className="h-454"
                ),
            ], className="mb-4 align-items-stretch"),
        ], fluid=True)
    ])