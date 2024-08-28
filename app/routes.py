from flask import render_template
from app import app
import csv
import os

# Path to the CSV file
CSV_FILE_PATH = os.path.join(app.root_path, '..', 'Data', 'electric_consumption.csv')

def read_csv_data(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

def calculate_emissions(energy_data):
    # This is a simplified calculation. Replace this with your actual calculation logic.
    total_consumption = 10
    
    # Assuming a simple conversion factor from kWh to CO2 emissions
    # This is a very simplified example - actual calculations would be more complex
    emission_factor = 0.5  # kg CO2 per kWh (this is an example value, use actual factors for your region)
    total_emissions = total_consumption * emission_factor

    return {
        'totalEmissions': total_emissions,
        'totalConsumption': total_consumption,
        'emissionFactor': emission_factor
    }

@app.route('/', methods=['GET'])
def dashboard():
    try:
        energy_data = read_csv_data(CSV_FILE_PATH)
        emissions_data = calculate_emissions(energy_data)
        return render_template('dashboard.html', emissions=emissions_data)
    except FileNotFoundError:
        return render_template('error.html', error=f'CSV file not found: {CSV_FILE_PATH}')
    except Exception as e:
        return render_template('error.html', error=f'An error occurred while processing emissions data: {str(e)}')