import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# ------------------ Constants ------------------
e = 1.602e-19  # Elementary charge in C
kb = 1.38e-23  # Boltzmann constant in J/K
me = 9.11e-31  # Electron mass in kg
mi = 1.67e-27  # Ion mass (proton) in kg
ProbeDia = 3e-3  # Probe diameter in m
Aprobe = np.pi * (ProbeDia / 2) ** 2
ne = 1e16
ni = 1e16
Tp = 0.03
V_min = -20
V_max = 20
V_points = 1000
V_range = np.linspace(V_min, V_max, V_points)

# ------------------ Helper Functions ------------------
def calculate_Vp(Te):
    return Te * np.log(np.sqrt(mi / (2 * np.pi * me)))

def calculate_Ie_sat(Te):
    Te_K = Te * 11600
    return 0.25 * e * ne * (np.sqrt((8 * kb * Te_K) / (np.pi * me))) * Aprobe

def calculate_Ii_sat(Te):
    Te_K = Te * 11600
    return 0.61 * e * ni * (np.sqrt((kb * Te_K) / mi)) * Aprobe

def Ie(V, Vp, Ie_sat, Te):
    exponent = (V - Vp) / Te
    exponent = np.clip(exponent, -700, 700)
    return np.where(V < Vp, Ie_sat * np.exp(exponent), Ie_sat)

def Ip(V, Vp, Ii_sat):
    exponent = (Vp - V) / Tp
    exponent = np.clip(exponent, -700, 700)
    return np.where(V < Vp, -Ii_sat, -Ii_sat * np.exp(exponent))

# ------------------ Dash App ------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Langmuir Probe Characteristics"),
    html.Label("Select Electron Temperature (Te) in eV:"),
    dcc.Slider(
        id='te-slider',
        min=0.1, max=2, step=0.05, value=1,
        marks={i: f"{i}" for i in np.arange(0.1, 2.1, 0.5)}
    ),
    dcc.Graph(id='langmuir-plot')
])

@app.callback(
    Output('langmuir-plot', 'figure'),
    [Input('te-slider', 'value')]
)
def update_plot(Te):
    Vp = calculate_Vp(Te)
    Ie_sat = calculate_Ie_sat(Te)
    Ii_sat = calculate_Ii_sat(Te)
    
    Ie_values = Ie(V_range, Vp, Ie_sat, Te)
    Ip_values = Ip(V_range, Vp, Ii_sat)
    It_values = Ie_values + Ip_values

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=V_range, y=Ie_values, mode='lines', name='Electron Current'))
    fig.add_trace(go.Scatter(x=V_range, y=Ip_values, mode='lines', name='Ion Current'))
    fig.add_trace(go.Scatter(x=V_range, y=It_values, mode='lines', name='Total Current'))
    fig.update_layout(
        title=f"Langmuir Probe Characteristics (Te={Te} eV)",
        xaxis_title="Voltage (V)",
        yaxis_title="Current (A)",
        template="plotly_white"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
