import pandas as pd

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




# # Clean up the data by removing commas in the numeric columns and converting them to numeric types
# columns_to_convert_new = ['RSEB_april', 'Solar_april', 'RSEB_may', 'Solar_may', 'RSEB_june', 'Solar_june', 'RSEB_july', 'Solar_july']

# # Remove commas and convert to numeric
# for column in columns_to_convert_new:
#     electric_data_new[column] = electric_data_new[column].astype(str).str.replace(',', '').astype(float)

# # Define CO2 emission factors (kg CO2 per kWh)
# RSEB_CO2_factor = 0.82
# Solar_CO2_factor = 0.048

# # Separate data for Mines and Plant
# mines_data = electric_data_new[electric_data_new['Location'] == 'Mines']
# plant_data = electric_data_new[electric_data_new['Location'] == 'Plant']

# # Calculate CO2 emissions for Mines and Plant for each source (RSEB and Solar)
# def calculate_emissions(data, location_name):
#     # Calculate total consumption for RSEB and Solar
#     total_RSEB_consumption = data[[f'RSEB_{month}' for month in ['april', 'may', 'june', 'july']]].sum().sum()
#     total_Solar_consumption = data[[f'Solar_{month}' for month in ['april', 'may', 'june', 'july']]].sum().sum()
    
#     # Calculate total CO2 emissions for RSEB and Solar
#     total_RSEB_emissions = total_RSEB_consumption * RSEB_CO2_factor
#     total_Solar_emissions = total_Solar_consumption * Solar_CO2_factor
    
#     return {
#         'Location': location_name,
#         'RSEB Emissions (kg CO2)': total_RSEB_emissions,
#         'Solar Emissions (kg CO2)': total_Solar_emissions,
#         'Total Emissions (kg CO2)': total_RSEB_emissions + total_Solar_emissions
#     }

# # Calculate emissions for Mines and Plant
# mines_emissions = calculate_emissions(mines_data, "Mines")
# plant_emissions = calculate_emissions(plant_data, "Plant")

# mines_emissions, plant_emissions