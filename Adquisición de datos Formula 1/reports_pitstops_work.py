import os
import time
import pandas as pd
import numpy as np
from Levenshtein import distance


def time_formater():
    """Toma todos los tiempos de la columna "Total time" y los convierte a segundos. 
Sustituyendo el formato mm:ss.ms por ss.ms. Y sumando los tiempos de los pilotos que no 
terminan primeros al tiempo del primero."""

    for year in range(2012,2024):
        for grandprix in os.listdir(f"Yearly grandprixs reports/{year}"):
            if grandprix.endswith("report.csv"):
                
                df = pd.read_csv(f"Yearly grandprixs reports/{year}/{grandprix}")
                
                first_time = df.loc[0,"Total time"].replace(":",",").split(",")
                total_first_time = 0
                
                for i in range(len(first_time)): # Convert the first time to seconds
                    total_first_time += float(first_time[i]) * 60**(len(first_time)-1-i)
                    
                df.loc[0,"Total time"] = total_first_time
                
                for row in range(1,len(df)):
                    row_time = str(df.loc[row,"Total time"])

                    if row_time != "" and row_time[-1].isnumeric(): 
                        row_time = row_time.replace("+","").replace(":","_").split("_")
                        
                        total_row_time = 0
                        
                        for i in range(len(row_time)): # Convert the row time to seconds
                            total_row_time += float(row_time[i]) * 60**(len(row_time)-1-i)
                            
                        df.loc[row,"Total time"] = total_row_time + total_first_time # Add the first time to the row time
                        
                df.to_csv(f"Yearly grandprixs reports/{year}/{grandprix}", index = False)
                        

def reports_pits_merge():
    """Une los report de cada carrera con el report de los pits de esa carrera."""
    
    for year in range(2012,2024):
        grandprixs = os.listdir(f"Yearly grandprixs reports/{year}")
        grandprixs.pop(grandprixs.index(f"Grandprix_urls_{year}.json"))
        try:
            grandprixs.pop(grandprixs.index(f"Belgian_2021_report.csv"))
            
        except ValueError:
            print("No se encontró el archivo de pits de la carrera de Bélgica 2021 por lo que se elimina de la lista de carreras.")
            
        for i in range(1,len(grandprixs),2):

            df_pits = pd.read_csv(f"Yearly grandprixs reports/{year}/{grandprixs[i-1]}") 
            df_report = pd.read_csv(f"Yearly grandprixs reports/{year}/{grandprixs[i]}")
            pits_drivers = df_pits["DriverID"].to_list()
            report_drivers = df_report["Driver"].to_list()
            
            for driver in pits_drivers:
                not_match = True
                matched_driver = ""
                
                for report_driver in report_drivers:
                    splitted_driver = report_driver.split(" ")
                    
                    if distance(driver,splitted_driver[-1].lower()) <= 2: # Compare the last name of the driver with the driverid in the pits report
                        df_pits.loc[df_pits["DriverID"] == driver,"Driver"] = report_driver
                        not_match = False
                        matched_driver = report_driver
                        
                        break
                
                if not_match: # In case the last name of the driver doesn't match with the driverid in the pits report, try to match fll name
                    for report_driver in report_drivers:
                        joined_driver = report_driver.replace(" ","_")
                        
                        if distance(driver,joined_driver.lower()) <= 3:
                            df_pits.loc[df_pits["DriverID"] == driver,"Driver"] = report_driver
                            matched_driver = report_driver
                            
                            break
                try:
                    report_drivers.pop(report_drivers.index(matched_driver))
                    
                except ValueError:
                    if matched_driver != "":
                        print(f"El piloto {matched_driver} no se encontró en el report de la carrera {grandprixs[i].replace(f'_{year}_report.csv','')} de {year}.")

            merged_df = pd.merge(left = df_report, right = df_pits, on = "Driver")
            
            missing_info = ["unknown",-1,-1,-1]
            for driver in report_drivers: # In case there are drivers in the report that are not in the pits report
                driver_info = df_report.loc[df_report["Driver"] == driver].iloc[0].values.tolist() # Get the info of the driver in the report

                driver_info.extend(missing_info) # Add the missing info
                
                merged_df.loc[len(merged_df)] = driver_info # Add the driver to the merged df
            
            location = grandprixs[i].replace(f"_{year}_report.csv","") # To get the location of the race for the name of the csv
            
            season = [year for i in range(len(merged_df))] #To identify the season
            merged_df["Season"] = season
            race_names = [location for i in range(len(merged_df))] # To identify the race
            merged_df["Place"] = race_names

            merged_df.sort_values(by = ["Position"],ascending = True ,inplace = True) # Sort the df by position
            
            merged_df.drop("DriverNumber", axis = 1, inplace = True) # Drop the driverid column
            
            merged_df.to_csv(f"Yearly grandprixs reports/{year}/{location}_{year}_complete.csv", index = False)
            
            
def csv_concater():
    """Concatena todos los csv de cada temporada en un solo csv. 
Y estos los concatena en un único csv."""

    for year in range(2012,2024):
        grandprixs = os.listdir(f"Yearly grandprixs reports/{year}")
        season_dfs = []
        
        for grandprix in grandprixs:
            if "complete" in grandprix:
                season_dfs.append(pd.read_csv(f"Yearly grandprixs reports/{year}/{grandprix}"))

        season_df = pd.concat(season_dfs, ignore_index = True)
        season_df.to_csv(f"Yearly grandprixs reports/{year}/{year}_season.csv", index = False)
        
    year_dfs = []
    
    for year in range(2012,2024):
        year_dfs.append(pd.read_csv(f"Yearly grandprixs reports/{year}/{year}_season.csv"))
    
    complete_database = pd.concat(year_dfs, ignore_index = True)
    complete_database.to_csv("Yearly grandprixs reports/complete_database.csv", index = False)