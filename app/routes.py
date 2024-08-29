from flask import render_template
# from flask_cors import CORS, cross_origin

from app import app
import csv
import os
import pandas as pd

# ===================================================================================================
# FUNCTIONS
# ===================================================================================================
def read_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df

def melt_electricity_df(data):
    df_melted = pd.melt(data, id_vars=['Location', 'Machine'], var_name='Month', value_name='Value')
    df_melted[['Source', 'Month']] = df_melted['Month'].str.split('_', expand=True)
    electric_data_new = df_melted
    return electric_data_new

def total_consumption(df, month, location, source):
    df_copy = df.copy()
    df_copy['Value'] = df['Value'].str.replace(',', '').astype(float)
    # Filter the dataframe based on the input parameters
    filtered_df = df_copy[(df_copy['Month'] == month.lower()) & 
                     (df_copy['Location'] == location) &
                     (df_copy['Source'] == source)]
    # Sum the values for the filtered rows
    total_consumption = float(filtered_df['Value'].sum())
    return total_consumption

def read_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df

def calculate_emissions(energy_data):
    months = energy_data['Month'].unique()
    rseb_factor = 0.82
    solar_factor = 0.048

    mine = {}
    for month in months:
        rseb_consumption =  total_consumption(energy_data, month=month, location="Mines", source="RSEB")
        solar_consumption = total_consumption(energy_data, month=month, location="Mines", source="Solar")
        mine[month] = {
                "solar_consumption": solar_consumption,
                "rseb_consumption": rseb_consumption,
                "rseb_co2_emissions": rseb_consumption*rseb_factor,
                "solar_co2_emissions": solar_consumption*solar_factor
            }

    plant = {}
    for month in months:
        rseb_consumption =  total_consumption(energy_data, month=month, location="Plant", source="RSEB")
        solar_consumption = total_consumption(energy_data, month=month, location="Plant", source="Solar")
        plant[month] = {
                "solar_consumption": solar_consumption,
                "rseb_consumption": rseb_consumption,
                "rseb_co2_emissions": rseb_consumption*rseb_factor,
                "solar_co2_emissions": solar_consumption*solar_factor
            }
    
    # Initialize sum
    total_emissions_plant = 0
    total_emissions_mine = 0

    # Iterate over the dictionary
    for month in months:
        total_emissions_plant += plant[month]['rseb_co2_emissions'] + plant[month]['solar_co2_emissions']

    for month in months:
        total_emissions_mine += mine[month]['rseb_co2_emissions'] + mine[month]['solar_co2_emissions']


    return {
        'totalEmissions': total_emissions_plant+total_emissions_mine,
        'totalEmissions_plant': total_emissions_plant,
        'totalEmissions_mine': total_emissions_mine,
        'plant': plant,
        'mine': mine
    }

# ===================================================================================================

# Path to the CSV file
CSV_FILE_PATH = os.path.join(app.root_path, '..', 'Data', 'electric_consumption.csv')


@app.route('/', methods=['GET'])
def dashboard():
    try:
        energy_data = read_csv_data(CSV_FILE_PATH)
        energy_data_melted = melt_electricity_df(energy_data)
        emissions_data = calculate_emissions(energy_data_melted)
        print(emissions_data)
        return render_template('dashboard.html', emissions= emissions_data)
    except FileNotFoundError:
        return render_template('error.html', error=f'CSV file not found: {CSV_FILE_PATH}')
    except Exception as e:
        return render_template('error.html', error=f'An error occurred while processing emissions data: {str(e)}')