from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

TIPOS_DEPORTE = ["conjunto", "individual", "para deporte"]
color_map = {
    "conjunto": "#5167F1",
    "individual": "#AAB8D8",
    "para deporte": "#001F54"
}


class DashboardCard:
    def __init__(
        self,
        card_type, # Tipo de tarjeta
        # Métrica
        icon_path=None, value=None, title_lines=None, border_color=None,
        # Género
        image_path=None, male_value=None, female_value=None,
        male_label="Masculino", female_label="Femenino",
        male_color="#293377", female_color="#A259C6",
        # Donut/Anillo
        labels=None, values=None, colors=None, donut_title=None,
        # Tendencia
        x_data=None, y_data=None, line_color="#5167F1", trend_title=None,
        # Deportes individuales
        deportes=None, tipo_colores=None
    ):
        self.card_type = card_type
        self.icon_path = icon_path
        self.value = value
        self.title_lines = title_lines
        self.border_color = border_color
        self.image_path = image_path
        self.male_value = male_value
        self.female_value = female_value
        self.male_label = male_label
        self.female_label = female_label
        self.male_color = male_color
        self.female_color = female_color
        self.labels = labels
        self.values = values
        self.colors = colors
        self.donut_title = donut_title
        self.x_data = x_data
        self.y_data = y_data
        self.line_color = line_color
        self.trend_title = trend_title
        self.deportes = deportes
        self.tipo_colores = tipo_colores

    def render(self):
        if self.card_type == "metric":
            return dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Img(src=self.icon_path, className="metric-icon"),
                        html.Div([
                            html.Span(self.value, className="metric-value"),
                            html.Div([
                                html.Div(line) for line in self.title_lines
                            ], className="metric-text")
                        ], className="metric-value-container")
                    ], className="metric-header"),
                    html.Div(className=f"metric-border-{self.border_color.replace('#', '')}")
                ]),
                className="dash-card metric-card"
            )

        elif self.card_type == "gender":
            return dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H5([
                            "Inscritos por ",
                            html.Strong("Género")
                        ], className="dash-card-title"),
                    ], className="gender-title"),
                    html.Div(className="dash-card-divider"),
                    html.Div([
                        html.Img(
                            src=self.image_path,
                            className="gender-img"
                        ),
                    ], className="gender-img-container"),
                    html.Div([
                        html.Span([
                            html.Span(className="legend-color", style={"backgroundColor": self.male_color}),
                            html.Span([
                                html.Span(self.male_label, className="gender-label"),
                                html.Br(),
                                html.Span(f"({self.male_value:,})", className="gender-value")
                            ])
                        ], className="gender-legend-item"),
                        html.Span([
                            html.Span(className="legend-color", style={"backgroundColor": self.female_color}),
                            html.Span([
                                html.Span(self.female_label, className="gender-label"),
                                html.Br(),
                                html.Span(f"({self.female_value:,})", className="gender-value")
                            ])
                        ], className="gender-legend-item")
                    ], className="gender-legend")
                ]),
                className="dash-card gender-card"
            )

        elif self.card_type == "donut":
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=self.labels,
                values=self.values,
                hole=0.6,
                marker_colors=self.colors,
                textinfo="percent",
                insidetextorientation='auto'
            ))
            fig.update_layout(
                showlegend=True,
                margin={"l": 20, "r": 20, "t": 40, "b": 40},
                font={"family": "Helvetica", "size": 12, "color": "#001226"},
                legend={"orientation": "v", "x": 1, "y": 0.5, "xanchor": "left"}
            )
            return dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H5(self.donut_title, className="dash-card-title"),
                    ], className="donut-title"),
                    html.Div(className="dash-card-divider"),
                    dcc.Graph(figure=fig, config={"displayModeBar": False}, className="dash-graph")
                ]),
                className="dash-card donut-card"
            )

        elif self.card_type == "trendline":
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=self.x_data,
                y=self.y_data,
                mode="lines+markers",
                name="Inscripciones",
                line={"color": self.line_color, "width": 2, "shape": "spline"}
            ))
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                title_pad={"t": 10, "l": 10},
                xaxis={
                    "title": {"text": "Mes", "font": {"size": 14, "color": "#828282"}},
                    "tickfont": {"size": 12, "color": "#828282"},
                    "gridcolor": "rgba(0,0,0,0)",
                    "showgrid": False,
                    "zeroline": False,
                },
                yaxis={
                    "title": {"text": ""},
                    "tickfont": {"size": 12, "color": "#828282"},
                    "gridcolor": "#d3d3d3",
                    "gridwidth": 1,
                    "showgrid": True,
                    "zeroline": False,
                    "griddash": "dash",
                },
                margin={"l": 40, "r": 40, "t": 60, "b": 40},
                font={"family": "Helvetica", "size": 12, "color": "#828282"},
                hovermode="x unified",
                legend={
                    "font": {"size": 12, "color": "#828282"},
                    "x": 1,
                    "y": 1,
                    "xanchor": "right",
                    "yanchor": "top",
                }
            )
            fig.add_annotation(
                xref="paper", yref="paper",
                x=-0.07, y=1.02,
                text="No. de inscritos",
                showarrow=False,
                font={"size": 14, "color": "#828282", "family": "Helvetica"},
                align="left"
            )
            return dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H5(self.trend_title, className="dash-card-title"),
                    ], className="trend-title"),
                    html.Div(className="dash-card-divider"),
                    dcc.Graph(figure=fig, config={"displayModeBar": False}, className="dash-graph")
                ]),
                className="dash-card trend-card"
            )
        elif self.card_type == "bar":
            fig = go.Figure()
            
            # Agregar barra para rural
            fig.add_trace(go.Bar(
                name='Rural',
                x=[dep.split()[0] for dep in self.x_data],  # Solo el primer nombre del departamento
                y=self.y_data[0],  # datos rurales
                marker_color='#E5C473',
                customdata=[[dep] for dep in self.x_data],
                hovertemplate='%{customdata[0]}<br>Rural: %{y}<extra></extra>'
            ))
            
            # Agregar barra para urbano
            fig.add_trace(go.Bar(
                name='Urbano',
                x=[dep.split()[0] for dep in self.x_data],  # Solo el primer nombre del departamento
                y=self.y_data[1],  # datos urbanos
                marker_color='#FFA354',
                customdata=[[dep] for dep in self.x_data],
                hovertemplate='%{customdata[0]}<br>Urbano: %{y}<extra></extra>'
            ))

            fig.update_layout(
                barmode='stack',
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=True,
                font={'family': 'Helvetica', 'size': 12, 'color': '#828282'},
                legend={
                    'orientation': 'h',
                    'x': 0.5,
                    'y': 1.15,
                    'xanchor': 'center'
                },
                xaxis=dict(
                    tickangle=-30,
                    automargin=True,
                    title='Departamento',
                    tickfont={'size': 12, 'color': '#828282'},
                    gridcolor='rgba(0,0,0,0)',
                    showgrid=False,
                    zeroline=False
                ),
                yaxis=dict(
                    title='No. de inscritos',
                    tickfont={'size': 12, 'color': '#828282'},
                    gridcolor='#d3d3d3',
                    gridwidth=1,
                    showgrid=True,
                    zeroline=False,
                    griddash='dash'
                ),
                margin={'l': 40, 'r': 40, 't': 60, 'b': 40}
            )

            return dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H5(self.trend_title, className='dash-card-title'),
                    ], className='trend-title'),
                    html.Div(className='dash-card-divider'),
                    dcc.Graph(figure=fig, config={'displayModeBar': False}, className='dash-graph')
                ]),
                className='dash-card'
            )
        elif self.card_type == "deportes_individuales":
            return self.render_deportes_individuales(self.deportes, self.tipo_colores)
        
        else:
            return html.Div("Tipo de tarjeta no soportado", style={"color": "red"})

    def render_deportes_individuales(self, deportes, tipo_colores):
        tipo_options = [
            {
                "label": html.Span([
                    html.Span(className="tipo-deporte-color", style={"backgroundColor": color}),
                    tipo
                ], className="tipo-deporte-label"),
                "value": tipo
            }
            for tipo, color in tipo_colores.items()
        ]
        return dbc.Card(
            dbc.CardBody([
                dcc.Checklist(
                    id="tipo-deporte-checklist",
                    options=[{"label": tipo.title(), "value": tipo} for tipo in TIPOS_DEPORTE],
                    value=TIPOS_DEPORTE,
                    inline=True,
                    inputStyle={"marginRight": "6px", "marginLeft": "12px"},
                    className="tipo-deporte-checklist"
                ),
                html.H5([
                    "Inscritos en ",
                    html.Strong("deportes individuales")
                ], className="dash-card-title"),
                html.Div(className="dash-card-divider"),
                dcc.Graph(
                    id="grafico-deportes-individuales",
                    config={"displayModeBar": False},
                    className="dash-graph"
                )
            ]),
            className="dash-card"
        )

