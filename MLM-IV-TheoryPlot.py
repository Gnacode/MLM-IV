import numpy as np
import plotly.subplots as sp
import plotly.graph_objects as go

# ------------------ Constant Declarations ------------------
# Physical constants
e = 1.602e-19  # Elementary charge in C
kb = 1.38e-23  # Boltzmann constant in J/K
me = 9.11e-31  # Electron mass in kg
mi = 1.67e-27  # Ion mass (assumed proton) in kg

# Experimental parameters
ProbeDia = 3e-3  # Probe diameter in m
Aprobe = np.pi * (ProbeDia / 2) ** 2  # Probe area in m^2
ne = 1e16  # Electron density in m^-3
ni = 1e16  # Ion density in m^-3

# Temperature 
Te_values = [0.1, 0.25, 0.5, 1, 2]  # Electron temperatures in eV
Tp = 0.03  # Ion temperature in eV

# Langmuir IV curve voltage parameters
V_min = -20  # Minimum voltage in V
V_max = 20  # Maximum voltage in V
V_points = 1000  # Number of points in voltage range

# Ion and electron current smoothing and leakage parameters, and due to plasma noise or averaging effects.
height_modifier = 1.0    #Electron current simulated max of theoretical max
stretch_modifier = 10.5  #Electron current simulation horizontal spread
slope_ion = 0.5e-5       # Slope for ion current leakage below Vp
slope_electron = 0.1e-4  # Slope for electron current leakage above Vp

# ------------------ End of Constant Declarations ------------------

# Generate voltage range
V_range = np.linspace(V_min, V_max, V_points)

# Helper functions
def calculate_Vp(Te):
    return Te * np.log(np.sqrt(mi / (2 * np.pi * me)))

def calculate_Ie_sat(Te):
    Te_K = Te * 11600  # Convert Te from eV to K
    return 0.25 * e * ne * (np.sqrt((8 * kb * Te_K) / (np.pi * me))) * Aprobe

def calculate_Ii_sat(Te):
    Te_K = Te * 11600  # Convert Te from eV to K
    return 0.61 * e * ni * (np.sqrt((kb * Te_K) / mi)) * Aprobe

# Define electron and ion current functions with leakage, using clipping for exponent
def Ie(V, Vp, Ie_sat, Te):
    exponent = (V - Vp) / Te
    exponent = np.clip(exponent, -700, 700)  # Cap the exponent to prevent overflow
    return np.where(V < Vp, Ie_sat * np.exp(exponent), Ie_sat)

def Ie_leakage(V, Vp, Ie_sat, Te):
    exponent = (V - Vp) / Te
    exponent = np.clip(exponent, -700, 700)  # Cap the exponent to prevent overflow
    base_current = np.where(V < Vp, Ie_sat * np.exp(exponent), Ie_sat)
    distance_from_Vp = np.maximum(V - Vp, 0)  # Only apply weight for V > Vp
    weight = distance_from_Vp / (max(V_range) - Vp)  # Weight increases with distance from Vp
    leakage_current = weight * slope_electron * (V - Vp)
    return base_current + np.where(V > Vp, leakage_current, 0)

def Ip(V, Vp, Ii_sat):
    exponent = (Vp - V) / Tp
    exponent = np.clip(exponent, -700, 700)  # Cap the exponent to prevent overflow
    return np.where(V < Vp, -Ii_sat, np.where(V > Vp, -Ii_sat * np.exp(exponent), -Ii_sat))

def Ip_leakage(V, Vp, Ii_sat):
    return np.where(V < Vp, -Ii_sat + slope_ion * (V - Vp), 0)

def smooth_transition_curve(Ie_values, Vp_index, height_modifier, stretch_modifier):
    Ie_values_scaled = height_modifier * Ie_values.copy()
    transition_start = max(0, Vp_index - int(5 * stretch_modifier))
    transition_end = min(len(Ie_values), Vp_index + int(10 * stretch_modifier))
    window_size = int(3 * stretch_modifier)
    
    for i in range(transition_start, transition_end):
        if i >= window_size and i < len(Ie_values_scaled) - window_size:
            Ie_values_scaled[i] = np.mean(Ie_values_scaled[i - window_size:i + window_size])
    
    return Ie_values_scaled

# Pre-calculate values
Vp_values = []
Ie_sat_values = []
Ii_sat_values = []

for Te in Te_values:
    Vp = calculate_Vp(Te)
    Ie_sat = calculate_Ie_sat(Te)
    Ii_sat = calculate_Ii_sat(Te)
    
    Vp_values.append(Vp)
    Ie_sat_values.append(Ie_sat)
    Ii_sat_values.append(Ii_sat)

# Create subplots with Plotly
fig = sp.make_subplots(rows=2, cols=2, subplot_titles=(
    'Electron Current with Leakage for Different Te Values',
    'Ion Current with Leakage for Different Te Values',
    'Derivative of Electron Current',
    'Total Current with Leakage for Different Te Values'
), vertical_spacing=0.15, horizontal_spacing=0.1)

colors = ['blue', 'orange', 'green', 'red', 'purple']

# Plot electron current with leakage and smoothed transition for each Te
for Te, Vp, Ie_sat, color in zip(Te_values, Vp_values, Ie_sat_values, colors):
    Ie_values = Ie(V_range, Vp, Ie_sat, Te)
    Vp_index = np.searchsorted(V_range, Vp)
    smooth_Ie_values = smooth_transition_curve(Ie_values, Vp_index, height_modifier, stretch_modifier)
    Ie_leakage = np.where(V_range > Vp, (V_range - Vp) * slope_electron, 0)
    
    fig.add_trace(go.Scatter(x=V_range, y=Ie_values, mode='lines', line=dict(color=color, width=2), 
                             name=f'Electron Current (Te={Te} eV)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=V_range, y=smooth_Ie_values, mode='lines', line=dict(color=color, dash='dot'), 
                             name=f'Smoothed Electron Current (Te={Te} eV)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=V_range, y=Ie_leakage, mode='lines', line=dict(color=color, dash='dashdot'), 
                             name=f'Electron Leakage Current (Te={Te} eV)'), row=1, col=1)

# Plot ion current with leakage for different Te values in subplot 2
for Te, Vp, Ii_sat, color in zip(Te_values, Vp_values, Ii_sat_values, colors):
    Ip_values = Ip(V_range, Vp, Ii_sat)
    Ip_leakage = np.where(V_range < Vp, (V_range - Vp) * slope_ion, 0)
    
    fig.add_trace(go.Scatter(x=V_range, y=Ip_values, mode='lines', line=dict(color=color, width=2), 
                             name=f'Ion Current (Te={Te} eV)'), row=1, col=2)
    fig.add_trace(go.Scatter(x=V_range, y=Ip_leakage, mode='lines', line=dict(color=color, dash='dot'), 
                             name=f'Ion Leakage Current (Te={Te} eV)'), row=1, col=2)

# Plot derivative of electron current in subplot 3
for Te, Vp, Ie_sat, color in zip(Te_values, Vp_values, Ie_sat_values, colors):
    Ie_values = Ie(V_range, Vp, Ie_sat, Te)
    dIe_dV = np.gradient(Ie_values, V_range)
    fig.add_trace(go.Scatter(x=V_range, y=dIe_dV, mode='lines', line=dict(color=color, dash='dot'), 
                             name=f'dIe/dV (Te={Te} eV)'), row=2, col=1)
    fig.add_trace(go.Scatter(x=[Vp, Vp], y=[min(dIe_dV), max(dIe_dV)], mode='lines', 
                             line=dict(color=color, dash='dot'), showlegend=False), row=2, col=1)
    fig.add_annotation(dict(x=Vp, y=max(dIe_dV) * 1.05, text=f'Vp={Vp:.2f} V', showarrow=False, 
                            font=dict(color=color), yshift=10, xref='x3', yref='y3'))

# Plot total probe characteristic with smoothed and leakage components for each Te value
for Te, Vp, Ie_sat, Ii_sat, color in zip(Te_values, Vp_values, Ie_sat_values, Ii_sat_values, colors):
    Ie_values = Ie(V_range, Vp, Ie_sat, Te)
    Vp_index = np.searchsorted(V_range, Vp)
    smooth_Ie_values = smooth_transition_curve(Ie_values, Vp_index, height_modifier, stretch_modifier)
    Ie_leakage = np.where(V_range > Vp, (V_range - Vp) * slope_electron, 0)
    Ip_values = Ip(V_range, Vp, Ii_sat)
    Ip_leakage = np.where(V_range < Vp, (V_range - Vp) * slope_ion, 0)

    It_values = smooth_Ie_values + Ie_leakage + Ip_values + Ip_leakage
    
    fig.add_trace(go.Scatter(x=V_range, y=It_values, mode='lines', line=dict(color=color), 
                             name=f'Total Current with Leakage (Te={Te} eV)'), row=2, col=2)

    zero_crossings = np.where(np.diff(np.sign(It_values)))[0]
    if len(zero_crossings) > 0:
        Vf_index = zero_crossings[0]
        Vf = V_range[Vf_index]
        fig.add_trace(go.Scatter(x=[Vf, Vf], y=[min(It_values), max(It_values)], mode='lines',
                                 line=dict(color=color, dash='dash'), showlegend=False), row=2, col=2)
        fig.add_annotation(dict(x=Vf, y=max(It_values) * 1.05, text=f'Vf={Vf:.2f} V', 
                                showarrow=False, font=dict(color=color), yshift=10, xref='x4', yref='y4'))

# Update layout
fig.update_layout(
    title='Langmuir Probe Characteristics with Leakage Currents and Smoothing Around Plasma Potential',
    template='plotly_white',
    height=1000
)

fig.show()
