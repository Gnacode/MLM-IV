import numpy as np
import plotly.graph_objects as go
import os
from datetime import datetime

# Flags
PLOTALL_SAMPLEDATA = True  # Set to True to plot all sample data
PLOT_AVERAGE_OF_SAMPLEDATA = False  # Set to True to plot the average of sample data

# Output directory
output_dir = "LMSIMData"
os.makedirs(output_dir, exist_ok=True)

# Physical constants
e = 1.602e-19  # Elementary charge in C
kb = 1.38e-23  # Boltzmann constant in J/K
me = 9.11e-31  # Electron mass in kg
mi = 1.67e-27  # Ion mass (assumed proton) in kg

# Experimental parameters
ProbeDia = 2.5e-3  # Probe diameter in m
ProbeLength = 0.000275  # Probe length in m (added length parameter)
Aprobe = (2 * np.pi * (ProbeDia / 2) * ProbeLength) + (np.pi * (ProbeDia / 2) ** 2)  # Probe area including cylindrical surface and end area in m^2
ne = 1e16  # Electron density in m^-3
ni = 1e16  # Ion density in m^-3

# Plasma Temperature for electrons and ions
Te_values = [0.1, 0.25, 0.5, 1, 2]  # Electron temperatures in eV
Tp = 0.03  # Ion temperature in eV

# Langmuir IV curve voltage parameters
V_min = -20  # Minimum voltage in V
V_max = 20  # Maximum voltage in V
V_points = 1000  # Number of points in voltage range

# Ion and electron current smoothing and leakage parameters, and due to plasma noise or averaging effects.
height_modifier = 0.9   # Electron current simulated max of theoretical max
stretch_modifier = 10.5 # Electron current simulation horizontal spread
slope_ion = 0.5e-5      # Slope for ion current leakage below Vp
slope_electron = 0.2e-4 # Slope for electron current leakage above Vp

# Noise parameters for simulated data
num_samples = 2  # Number of noisy samples to generate
noise_amplitude = 0.00018  # Amplitude of Gaussian noise

# Setting the Langmuir IV curve voltage range
V_range = np.linspace(V_min, V_max, V_points)

# Helper functions
def calculate_Vp(Te):
    return Te * np.log(np.sqrt(mi / (2 * np.pi * me)))

# Calculate the electron saturation current using eV converted to Kelvin
def calculate_Ie_sat(Te):
    Te_K = Te * 11600  # Convert Te from eV to K
    return 0.25 * e * ne * (np.sqrt((8 * kb * Te_K) / (np.pi * me))) * Aprobe

# Calculate the ion saturation current using eV converted to Kelvin
def calculate_Ii_sat(Te):
    Te_K = Te * 11600  # Convert Te from eV to K
    return 0.61 * e * ni * (np.sqrt((kb * Te_K) / mi)) * Aprobe

# Electron current
def Ie(V, Vp, Ie_sat, Te):
    exponent = (V - Vp) / Te
    exponent = np.clip(exponent, -700, 700)  # Limit exponent to prevent overflow
    return np.where(V < Vp, Ie_sat * np.exp(exponent), Ie_sat)

# Electron leakage current above Vp
def Ie_leakage(V, Vp, Ie_sat, Te):
    exponent = (V - Vp) / Te
    exponent = np.clip(exponent, -700, 700)  # Limit exponent to prevent overflow
    base_current = np.where(V < Vp, Ie_sat * np.exp(exponent), Ie_sat)
    distance_from_Vp = np.maximum(V - Vp, 0)
    weight = distance_from_Vp / (max(V_range) - Vp)
    leakage_current = weight * slope_electron * (V - Vp)
    return base_current + np.where(V > Vp, leakage_current, 0)

# Ion current
def Ip(V, Vp, Ii_sat):
    exponent = (Vp - V) / Tp
    exponent = np.clip(exponent, -700, 700)  # Limit exponent to prevent overflow
    return np.where(V < Vp, -Ii_sat, np.where(V > Vp, -Ii_sat * np.exp(exponent), -Ii_sat))

# Ion leakage current below Vp
def Ip_leakage(V, Vp, Ii_sat):
    return np.where(V < Vp, -Ii_sat + slope_ion * (V - Vp), 0)


# Experimental artifact settings for the Ie current which rounds the "knee"
def smooth_transition_curve(Ie_values, Vp_index, height_modifier, stretch_modifier):
    Ie_values_scaled = height_modifier * Ie_values.copy()
    transition_start = max(0, Vp_index - int(5 * stretch_modifier))
    transition_end = min(len(Ie_values), Vp_index + int(10 * stretch_modifier))
    window_size = int(3 * stretch_modifier)
    
    for i in range(transition_start, transition_end):
        if i >= window_size and i < len(Ie_values_scaled) - window_size:
            Ie_values_scaled[i] = np.mean(Ie_values_scaled[i - window_size:i + window_size])
    
    return Ie_values_scaled

# Additional function for adding Gaussian noise with highest amplitude around Vp
def add_gaussian_noise(It_values, V_range, Vp, num_samples=num_samples, noise_amplitude=noise_amplitude):
    distance_from_Vp = np.abs(V_range - Vp)
    max_distance = max(distance_from_Vp)
    noise_factor = 1 - (distance_from_Vp / max_distance)
    noisy_samples = []
    for _ in range(num_samples):
        noise = noise_factor * np.random.normal(0, noise_amplitude, size=It_values.shape)
        noisy_samples.append(It_values + noise)
    return noisy_samples

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

# Generate a new figure for the noisy plot
fig_noisy = go.Figure()

# Loop through Te values and generate the noisy total current plot for each
colors = ['blue', 'orange', 'green', 'red', 'purple']
for Te, Vp, Ie_sat, Ii_sat, color in zip(Te_values, Vp_values, Ie_sat_values, Ii_sat_values, colors):
    # Calculate smoothed electron current with leakage for total current
    Ie_values = Ie(V_range, Vp, Ie_sat, Te)
    Vp_index = np.searchsorted(V_range, Vp)
    smooth_Ie_values = smooth_transition_curve(Ie_values, Vp_index, height_modifier, stretch_modifier)
    
    # Calculate the electron leakage current with weighting
    Ie_leakage = np.where(V_range > Vp, (V_range - Vp) * slope_electron, 0)
    
    # Calculate the ion current with leakage
    Ip_values = Ip(V_range, Vp, Ii_sat)
    Ip_leakage = np.where(V_range < Vp, (V_range - Vp) * slope_ion, 0)

    # Combine smoothed electron current, electron leakage, ion current, and ion leakage for total
    It_values = smooth_Ie_values + Ie_leakage + Ip_values + Ip_leakage
    
    # Add Gaussian noise and calculate the average of the samples
    noisy_samples = add_gaussian_noise(It_values, V_range, Vp)
    averaged_noisy_sample = np.mean(noisy_samples, axis=0)

    # Plot all noisy samples if PLOTALL_SAMPLEDATA is True
    if PLOTALL_SAMPLEDATA:
        for noisy_sample in noisy_samples:
            fig_noisy.add_trace(go.Scatter(x=V_range, y=noisy_sample, mode='markers',
                                           marker=dict(color=color, size=3),
                                           showlegend=False))

    # Plot the averaged noisy sample if PLOT_AVERAGE_OF_SAMPLEDATA is True
    if PLOT_AVERAGE_OF_SAMPLEDATA:
        fig_noisy.add_trace(go.Scatter(x=V_range, y=averaged_noisy_sample, mode='markers', 
                                       marker=dict(color=color, size=6), 
                                       showlegend=False))

    # ADDITION: Theoretical summed curve (Ie + Ii)
    theoretical_total_current = Ie_values + Ip_values  # Theoretical total current without leakage or smoothing
    fig_noisy.add_trace(go.Scatter(
        x=V_range,
        y=theoretical_total_current,
        mode='lines',
        line=dict(color=color, width=1),
        name=f"Theoretical Total Current (Te={Te} eV)"
    ))

    # Save the averaged noisy sample in 2-row format
    data_to_save = np.array([V_range, averaged_noisy_sample])
    filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-LangmuirSIM_eV{Te}_averaged_noisy.npy"
    filepath = os.path.join(output_dir, filename)
    np.save(filepath, data_to_save)
    print(f"Averaged noisy data saved for Te={Te} eV in file: {filepath}")

    # Save the theoretical data in 2-row format
    theory_data_to_save = np.array([V_range, theoretical_total_current])
    theory_filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-LangmuirSIM_eV{Te}_theory.npy"
    theory_filepath = os.path.join(output_dir, theory_filename)
    np.save(theory_filepath, theory_data_to_save)
    print(f"Theoretical data saved for Te={Te} eV in file: {theory_filepath}")

# Update layout for the noisy plot
fig_noisy.update_layout(
    title="Noisy Total Current with Resampling around Plasma Potential",
    xaxis_title="Probe Voltage (V)",
    yaxis_title="Probe Current (A)",
    template="plotly_white"
)

# Show the noisy plot
fig_noisy.show()
