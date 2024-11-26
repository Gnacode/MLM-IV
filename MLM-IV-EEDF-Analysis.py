import numpy as np
import plotly.graph_objs as go
import plotly.subplots as sp
from scipy.optimize import curve_fit, least_squares
from scipy.integrate import simpson, trapezoid

# Constants for EEDF calculation
q_e = 1.602e-19  # Elementary charge in C
m_e = 9.109e-31  # Electron mass in kg
A_probe = 1.41372e-5  # Probe area in m^2

# Load the data
file_path = 'LMSIMData\\20241126-112819-LangmuirSIM_eV2_theory.npy'
data = np.load(file_path, allow_pickle=True)
voltage = data[0]
current = data[1]

# Define constants
Vp = 5.68  # Plasma potential in volts

# Smooth the data using a moving average
window_size = 5
smoothed_current = np.convolve(current, np.ones(window_size) / window_size, mode='same')

# Define a new fitting function for improved fit
def improved_fit_function(x, a, b, c, d):
    return a * np.tanh(b * (x - c)) + d

# Fit the new model to the middle segment with adjusted parameter guesses for better fitting
middle_voltage_range = (voltage >= -15) & (voltage <= 15)  # Expanded range for better fitting
initial_guess = [1, 0.5, 0, 0]  # Adjusted initial parameter guesses
popt_improved, _ = curve_fit(improved_fit_function, voltage[middle_voltage_range], smoothed_current[middle_voltage_range], p0=initial_guess)
improved_fit = improved_fit_function(voltage, *popt_improved)

# Define linear fit functions for lower and higher voltage ranges
def linear_fit(x, a, b):
    return a * x + b

# Fit the lower and higher voltage ranges
low_voltage_range = voltage < -15
high_voltage_range = voltage > 15
popt_low, _ = curve_fit(linear_fit, voltage[low_voltage_range], smoothed_current[low_voltage_range])
popt_high, _ = curve_fit(linear_fit, voltage[high_voltage_range], smoothed_current[high_voltage_range])

# Create leakage model for the entire voltage range using piecewise linear functions
leakage_model = np.piecewise(voltage, 
                             [voltage < -15, voltage > 15], 
                             [lambda x: linear_fit(x, *popt_low),
                              lambda x: linear_fit(x, *popt_high),
                              0])  # No adjustment for mid-range voltage

# Calculate the difference between the improved fit and leakage model
difference = improved_fit - leakage_model

# Identify the crossing points for the regions to adjust
crossing_left = np.argmax((voltage >= 0) & (difference > 0))  # Start point to adjust on the left from 0 volts
crossing_right = np.argmax((voltage > Vp) & (difference < 0))  # Start point to adjust on the right

# Initialize the adjusted current as a copy of the original current
adjusted_current = np.copy(current)

# Apply corrections towards Vmin starting from crossing_left, removing a fixed value to ensure visible change
for i in range(crossing_left):
    adjusted_current[i] -= 0.5 * current[i]  # Remove 50% of the original current for a more pronounced effect

# Apply corrections towards Vmin starting from crossing_right, leaving midsection untouched
for i in range(crossing_right, len(voltage)):
    adjustment = 0.5 * difference[i]
    adjusted_current[i] += adjustment

# Fit the improved model to the adjusted current using least_squares for a more flexible optimization
def adjusted_improved_fit_function(x, a, b, c, d):
    return a * np.tanh(b * (x - c)) + d

def residuals(params, x, y):
    return adjusted_improved_fit_function(x, *params) - y

initial_guess_adjusted = [1, 0.5, 0, 0]  # Adjusted initial parameter guesses for the fit
result = least_squares(residuals, initial_guess_adjusted, args=(voltage[middle_voltage_range], adjusted_current[middle_voltage_range]))
popt_adjusted_improved = result.x
adjusted_improved_fit = adjusted_improved_fit_function(voltage, *popt_adjusted_improved)

# Calculate first and second derivatives of the fitted improved function
first_derivative = np.gradient(adjusted_improved_fit, voltage)
second_derivative = np.gradient(first_derivative, voltage)

# Create a Plotly subplot figure
fig = sp.make_subplots(rows=2, cols=2, subplot_titles=(
    "Current with Refined Leakage Correction (Adjusted)",
    "First Derivative of Adjusted Improved Fit",
    "Second Derivative of Adjusted Improved Fit",
    "Electron Energy Distribution Function (EEDF)"))

# Plot original and adjusted currents
fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name='Original Current', line=dict(dash='dash', color='blue')), row=1, col=1)
fig.add_trace(go.Scatter(x=voltage, y=leakage_model, mode='lines', name='Leakage Model', line=dict(dash='dot', color='red')), row=1, col=1)
fig.add_trace(go.Scatter(x=voltage, y=adjusted_current, mode='lines', name='Adjusted Current', line=dict(color='green')), row=1, col=1)
fig.add_trace(go.Scatter(x=voltage, y=adjusted_improved_fit, mode='lines', name='Adjusted Improved Fit', line=dict(color='orange')), row=1, col=1)

# Plot first derivative
fig.add_trace(go.Scatter(x=voltage, y=first_derivative, mode='lines', name='First Derivative', line=dict(color='purple')), row=1, col=2)

# Plot second derivative
fig.add_trace(go.Scatter(x=voltage, y=second_derivative, mode='lines', name='Second Derivative', line=dict(color='brown')), row=2, col=1)

# Plot EEDF calculation
analysis_range = (voltage[middle_voltage_range] >= Vp - 2) & (voltage[middle_voltage_range] <= 20)  # Expanded range for EEDF analysis
voltages_for_eedf = voltage[middle_voltage_range][analysis_range]
second_derivative_middle = second_derivative[middle_voltage_range]
second_derivative_for_eedf = second_derivative_middle[analysis_range]

# Filter out negative energies to avoid invalid sqrt operations
energies_eV = voltages_for_eedf - Vp
positive_energy_indices = energies_eV > 0
energies_eV = energies_eV[positive_energy_indices]
second_derivative_for_eedf = second_derivative_for_eedf[positive_energy_indices]

# Update scaling factor and adjust the EEDF formula
scaling_factor = 5.5e19  # Increased scaling factor for better EEDF magnitude
eedf = np.abs(scaling_factor * (2 / (A_probe * q_e)) * np.sqrt(2 * m_e * energies_eV * q_e) * second_derivative_for_eedf)

fig.add_trace(go.Scatter(x=energies_eV, y=eedf, mode='lines', name='EEDF', line=dict(color='black')), row=2, col=2)

# Update layout
fig.update_layout(title='Langmuir Probe Analysis', height=800, width=1200)
fig.update_xaxes(title_text='Voltage (V)', row=1, col=1)
fig.update_yaxes(title_text='Current (I)', row=1, col=1)
fig.update_xaxes(title_text='Voltage (V)', row=1, col=2)
fig.update_yaxes(title_text='dI/dV', row=1, col=2)
fig.update_xaxes(title_text='Voltage (V)', row=2, col=1)
fig.update_yaxes(title_text='d^2I/dV^2', row=2, col=1)
fig.update_xaxes(title_text='Energy (eV)', row=2, col=2)
fig.update_yaxes(title_text='EEDF', row=2, col=2)

# Show the figure
fig.show()

# Calculate electron density (n_e) and temperature (T_e)
integrand_density = eedf / np.sqrt(energies_eV)
n_e_simpson = simpson(integrand_density, x=energies_eV)  # Simpson's rule
n_e_trapz = trapezoid(integrand_density, x=energies_eV)   # Trapezoidal rule

integrand_temperature = (energies_eV ** (3/2)) * eedf
T_e_simpson = (2 / (3 * n_e_simpson)) * simpson(integrand_temperature, x=energies_eV)  # Using Simpson
T_e_trapz = (2 / (3 * n_e_trapz)) * trapezoid(integrand_temperature, x=energies_eV)    # Using Trapezoidal

# Output the calculated values
print("Electron Density (n_e) [Simpson]:", n_e_simpson)
print("Electron Density (n_e) [Trapz]:", n_e_trapz)
print("Electron Temperature (T_e) [Simpson]:", T_e_simpson, "eV")
print("Electron Temperature (T_e) [Trapz]:", T_e_trapz, "eV")

# Convert T_e to Kelvin for interpretation
T_e_kelvin_simpson = T_e_simpson * 11600
T_e_kelvin_trapz = T_e_trapz * 11600
print("Electron Temperature (T_e) [Simpson]:", T_e_kelvin_simpson, "K")
print("Electron Temperature (T_e) [Trapz]:", T_e_kelvin_trapz, "K")
