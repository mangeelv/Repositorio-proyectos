import re
import scrapy
import json
import subprocess
import time
import os
import platform
import numpy as np
import pandas as pd 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer




def report_paths(year) -> list: 
    """Extrae las urls de los report de cada carrera de un año y las devuelve en una lista."""
    
    with open(f"Yearly grandprixs reports/{year}/Grandprix_urls_{year}.json", "r") as file:
        yearly_grandprixs = json.load(file)
    
    paths = []
    for grandprix in yearly_grandprixs:
        paths.append(grandprix["URL"])

    return paths


def report_csvs():
    """Extrae las urls de los report, guardándolas en jsons por año.
Extrae el csv de cada carrera y lo almacena en las carpetas por año.
La estructura de carpetas es la siguiente:
    - Yearly grandprixs reports
        - 2012
            - Grandprix_urls_2012.json
            - Australia_2012_report.csv
            - ...
        - ..."""
    
    try:
        
        answer = platform.system().lower()
                
        if answer == "windows": # In case the OS is Windows
            urls = "from grandprixs_urls import obtain_urls; obtain_urls(); exit()" # Run grandprixs_urls.py
            command = ["start", "cmd", "/k", "python", "-c", urls]
            process = subprocess.Popen(command, shell = True)
            process.wait()
            
        else: # In case the OS is Mac
            current_dir = os.getcwd()
            command = f"""
            tell application "Terminal"
                activate
                do script "cd {current_dir} && python3 grandprixs_urls.py"
            end tell
            """

            subprocess.run(['osascript', '-e', command])
    
    except Exception as e:
        print(f"Error running grandprixs_urls: {e}")
            
    print("Esperando a que se creen los jsons y ficheros correctamente...")
    time.sleep(10) # Wait for the jsons to be created 
    
    configure_logging()
    
    process = CrawlerProcess()

    
    deferreds = []
    for year in range(2012, 2024): # Runs the spider for each year
        deferred = process.crawl(ReportSpider, start_urls=report_paths(year))
        deferreds.append(deferred)

    try:
        deferred_list = defer.DeferredList(deferreds)
        deferred_list.addBoth(lambda _: reactor.stop()) # Stop the reactor when the spider finishes
        reactor.run()
        
    except Exception as e:
        print(f"Error running ReportSpider: {e}")
        


    
class ReportSpider(scrapy.Spider):
    
    name = "Reports"
    start_urls = []
    
    
    def parse(self, response):
        
        expected_last_column = "Points"
        table_number = 0
        while response.css("table")[table_number].css("tr")[0].css("th::text").getall() == []: # In case there is a table with no header
            table_number += 1
        
        try:
            while expected_last_column not in response.css("table")[table_number].css("tr")[0].css("th::text").getall()[-1].replace("\n","") and expected_last_column not in response.css("table")[table_number].css("tr")[0].css("th::text").getall()[-2].replace("\n",""): # In case the last or the second last columns are not the expected
                table_number += 1
                
        except IndexError: # In case there is only one table
            while expected_last_column not in response.css("table")[table_number].css("tr")[0].css("th::text").getall()[-1].replace("\n",""):
                table_number += 1
        
        if len(response.css("table")[table_number].css("tr")) < 10: # In case the table is too short
            table_number = table_number - 2
        
        number_rows_first_table = len(response.css("table")[table_number].css("tr").getall())
        number_rows_second_table = len(response.css("table")[table_number+1].css("tr").getall())
        number_columns_first_table = len(response.css("table")[table_number].css("tr")[0].css("th::text").getall())
        number_columns_second_table = len(response.css("table")[table_number+1].css("tr")[0].css("th::text").getall())
        
        if number_rows_first_table == number_rows_second_table and number_columns_first_table > number_columns_second_table: # In case the first table has more information than needed
            table_number = table_number + 1 
            
        table = response.css("table")[table_number]
        race_info = []

        for i in range(1,len(table.css("tr"))-1):
            
            if None != table.css("tr")[i].css("a::attr(title)").get() and "Fastest lap" not in table.css("tr")[i].css("a::attr(title)").get(): # In case there is a Fastest lap row
                
                driver_info = {}
                
                try:
                    pos = table.css("tr")[i].css("th::text").get().replace("\n","") # Position
                    
                    if pos.isnumeric():
                        pos = int(pos)
                        
                    else:
                        pos = np.nan
                
                except AttributeError:
                    pos = np.nan
                
                try:
                    num = int(table.css("tr")[i].css("td::text").getall()[0].replace("\n","").replace(" ","")) # Car number
                    
                except ValueError:
                    num = np.nan
                
                driver = table.css("tr")[i].css("td")[1].css("a::text").get().replace("\n","") # Driver
                
                constructor = table.css("tr")[i].css("td")[2].css("a::text").getall() # Builder
                
                try:
                    laps = int(table.css("tr")[i].css("td::text").getall()[-4].replace("\n","")) # Laps 
                
                except ValueError:
                    laps = int(table.css("tr")[i].css("td::text").getall()[-5].replace("\n",""))
                
                total_time = table.css("tr")[i].css("td::text").getall()[-3].replace("\n","") # Total time
                
                if len(total_time) <= 2:
                    total_time = table.css("tr")[i].css("td::text").getall()[-4].replace("\n","")
                
                grid = table.css("tr")[i].css("td::text").getall()[-2].replace("\n","") # Grid
                
                try:
                    points = float(table.css("tr")[i].css("b::text")[-1].get().replace("\n","").replace("<","").replace("/","").replace("td>","").replace("b>","")) # Points
                
                except IndexError:
                    points = 0
                    
                driver_info["Position"] = pos # Save the information in a dictionary
                driver_info["Number"] = num
                driver_info["Driver"] = driver
                driver_info["Constructor"] = constructor
                driver_info["Laps"] = laps
                driver_info["Total time"] = total_time
                driver_info["Grid"] = grid
                driver_info["Points"] = points
                
                race_info.append(driver_info)
            
        race_df = pd.DataFrame(race_info) # Create a dataframe with the information
        
        try:
            year_pattern = re.compile(r"/(\d{4})_(\w*|S%C3%A3o_Paulo)_Grand_Prix") # Extract the year from the url
            match = year_pattern.search(response.url)
            year = match.group(1)
            country = match.group(2)
            
            if country == "Brazilian":
                country = "S%C3%A3o_Paulo"
            
            race_df.to_csv(f"Yearly grandprixs reports/{year}/{country}_{year}_report.csv", index = False) # Save the dataframe as a csv file

            
        except AttributeError:
            aniversary_pattern = re.compile(r"/(\d*)th_Anniversary_Grand_Prix") # Extract the year from the url
            aniversary_match = aniversary_pattern.search(response.url)
            aniversary = aniversary_match.group(1)

            year_aniversary = response.css("table")[1].css("tr")[0].css("a::attr(title)").get()[0:4] # Extract the year from the previous race

            race_df.to_csv(f"Yearly grandprixs reports/{year_aniversary}/{aniversary}th_Anniversary_{year_aniversary}_report.csv", index = False)