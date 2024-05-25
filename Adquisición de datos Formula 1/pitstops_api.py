import requests
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import os




def parseador_pitstops(url: str):
    """Extrae los datos de los pitstops de una carrera de la url y los devuelve en un dataframe."""
    
    try:
        xml_data = requests.get(url).content
        root = ET.fromstring(xml_data)
        namespace = {'ns': 'http://ergast.com/mrd/1.5'}
        
        # Obtener el tipo de carrera de la URL
        race_url = root.find('.//ns:Race', namespace).get('url')
        race_type = race_url.split("/")[-1]  # Extraer la parte final de la URL
        
        pitstops_data = []
        pitstops_list = root.find('.//ns:PitStopsList', namespace)
        
        for pitstop in pitstops_list.findall('ns:PitStop', namespace):
            driver_id = pitstop.get('driverId')
            stop_number = pitstop.get('stop')
            lap = pitstop.get('lap')
            time = pitstop.get('time')
            duration = pitstop.get('duration')
            
            # Agregar el tipo de carrera a los datos de pitstop
            pitstops_data.append({'DriverID': driver_id, 'Stop': stop_number, 'Lap': lap, 'Time': time, 'Duration': duration, 'RaceType': race_type})
        
        pitstops_df = pd.DataFrame(pitstops_data)
        return pitstops_df
    
    except AttributeError:
        return pd.DataFrame()   


def get_all_pitstops():
    """Extrae los datos de los pitstops de todas las carreras de todos los años y los devuelve en un dataframe."""
    
    # esta parte tarda un poco (3 mins)
    dfs_years = {'2012': [], '2013': [], '2014': [], '2015': [], '2016': [], '2017': [], '2018': [], '2019': [], '2020': [], '2021': [], '2022': [], '2023': []}
    for year in dfs_years.keys():
        print(f'Obteniendo pitstops del año: {year}...')
        ronda = 1
        while ronda != 25:
            offset = 0
            while True:
                final = f'?limit=30&offset={offset}'
                url = f'https://ergast.com/api/f1/{year}/{ronda}/pitstops{final}'
                pitstops_df = parseador_pitstops(url)
                if not pitstops_df.empty:
                    pitstops_df['year'] = [year for i in range(len(pitstops_df))]
                    pitstops_df['round'] = [ronda for i in range(len(pitstops_df))]
                    dfs_years[year].append(pitstops_df)
                    offset += 30
                else:
                    break
            ronda += 1
    all_pitstops = pd.concat([df for dfs_list in dfs_years.values() for df in dfs_list], ignore_index=True)
    return all_pitstops

def parseador_drivers(url:str):
    """Extrae los datos de los pilotos de una carrera de la url y los devuelve en un dataframe."""
    
    try: 
        xml_data = requests.get(url).content
        root = ET.fromstring(xml_data)
        namespace = {'ns': 'http://ergast.com/mrd/1.5'}
        
        driver_id = root.find('.//ns:Driver', namespace).get('driverId')
        
        code = root.find('.//ns:Driver', namespace).get('code')
        
        # url = root.find('.//ns:Driver', namespace).get('url')
        permanent_number = root.find('.//ns:PermanentNumber', namespace).text
        
        given_name = root.find('.//ns:GivenName', namespace).text
        
        family_name = root.find('.//ns:FamilyName', namespace).text
        
        date_of_birth = root.find('.//ns:DateOfBirth', namespace).text
        
        nationality = root.find('.//ns:Nationality', namespace).text
        
        data = {
            'DriverID': [driver_id],
            'Code': [code],
            'PermanentNumber': [permanent_number],
            'GivenName': [given_name],
            'FamilyName': [family_name],
            'DateOfBirth': [date_of_birth],
            'Nationality': [nationality]
        }
        
        # data = {
        #     'DriverID': [driver_id],
        #     'Code': [code],
        #     'URL': [url],
        #     'PermanentNumber': [permanent_number],
        #     'GivenName': [given_name],
        #     'FamilyName': [family_name],
        #     'DateOfBirth': [date_of_birth],
        #     'Nationality': [nationality]
        # }
        
        df = pd.DataFrame(data)
        return df
    
    except AttributeError:
        return driver_id
    
    
def get_drivers(all_pitstops):
    """Extrae los datos de los pilotos de todas las carreras de todos los años y los devuelve en un dataframe."""
    
    driver_ids = list(set(all_pitstops['DriverID']))
    drivers_dfs = []
    pilotos_retirados = [] # Los pilotos retirados no tienen numero y salta error 
    
    for driverid in driver_ids:
        url = f'https://ergast.com/api/f1/drivers/{driverid}'
        resultado = parseador_drivers(url)
        
        if type(resultado) ==  str:
            pilotos_retirados.append(resultado)
            
        else:
            drivers_dfs.append(resultado)

    drivers_df = pd.concat(drivers_dfs)
    
    return drivers_df,pilotos_retirados


def get_mapeo(drivers_df,pilotos_retirados):
    """Crea un mapeo entre los ids y los numeros de los pilotos."""
    
    retirados_mapeo = pd.DataFrame()
    retirados_mapeo['DriverID'] = pilotos_retirados
    retirados_mapeo['PermanentNumber'] = [np.nan for i in range(len(pilotos_retirados))]
    
    activos_mapeo = pd.DataFrame()
    activos_mapeo['DriverID'] = drivers_df['DriverID']
    activos_mapeo['PermanentNumber'] = drivers_df['PermanentNumber']
    
    mapeo_df = pd.concat([activos_mapeo,retirados_mapeo])
    mapeo_df.loc[mapeo_df['DriverID'] == 'max_verstappen', 'PermanentNumber'] = '33, 1' # Consideramos que verstappen cambió de número 
    
    return mapeo_df


def get_all_races_dataframes(all_pitstops,mapeo_df):
    """Crea un dataframe por cada carrera con la información de los pilotos que participaron en ella."""
    
    all_pitstops['Duration'] = pd.to_numeric(all_pitstops['Duration'],errors='coerce')
    carreras = all_pitstops['RaceType'].unique().tolist()
    races_dataframes = []
    
    for carrera in carreras:
        df_dic = {"DriverID":[], "DriverNumber":[], "NPitstops":[], "MedianPitStopDuration":[]}
        pitstops_carrera = all_pitstops[all_pitstops['RaceType'] == carrera]
        driver_ids = pitstops_carrera['DriverID'].unique().tolist()
        
        for id in driver_ids:
            diver_number = mapeo_df.loc[mapeo_df['DriverID'] == id, 'PermanentNumber'].values[0]
            npitstops = len(pitstops_carrera[pitstops_carrera['DriverID'] == id])
            pitstop_durations = pitstops_carrera[pitstops_carrera['DriverID'] == id]['Duration']
            
            if not pitstop_durations.isnull().all():
                median_pitstop_duration = pitstop_durations.median()
                
            else:
                median_pitstop_duration = np.nan 
                
            df_dic['DriverID'].append(id)
            df_dic['DriverNumber'].append(diver_number)
            df_dic['NPitstops'].append(npitstops)
            df_dic['MedianPitStopDuration'].append(median_pitstop_duration)
            
        df = pd.DataFrame(df_dic)
        races_dataframes.append(df)
        
    return races_dataframes

def guardar(races_dataframes,all_pitstops):
    """Guarda los dataframes de cada carrera en un csv."""
    
    carreras = all_pitstops['RaceType'].unique().tolist()
    
    if not os.path.exists('Yearly grandprixs reports'):
        os.mkdir('Yearly grandprixs reports')
        
    for i in range(len(races_dataframes)):
        carrera_name = carreras[i].replace('Grand_Prix','pitsops')
        
        if carrera_name == '70th_Anniversary_pitsops': # Esta carrera es del 2020
            if not os.path.exists('Yearly grandprixs reports/2020'):
                os.mkdir('Yearly grandprixs reports/2020')
            races_dataframes[i].to_csv(f'Yearly grandprixs reports/2020/70th_Anniversary_2020_pitstops.csv',index=False)

        else:
            carrera_name = carrera_name.split('_')
            year = carrera_name[0]
            country_name = ''
            
            for i in range(1,len(carrera_name)-1):
                country_name += carrera_name[i] + '_'
            
            if country_name == 'Brazilian_': # Sao Paulo es la unica carrera que tiene un nombre con acento
                country_name = 'S%C3%A3o_Paulo_'
                
            carrera_name = country_name + year + '_' + 'pitstops'

            if not os.path.exists(f'Yearly grandprixs reports/{year}'):
                os.mkdir(f'Yearly grandprixs reports/{year}')
                
            ruta = f'Yearly grandprixs reports/{year}/{carrera_name}.csv'
            races_dataframes[i].to_csv(ruta,index=False)


        
    
def obtain_pitstops():
    """Función principal que obtiene los pitstops de todas las carreras y las guarda en un csv."""
    
    print('Obteniendo pitstops...')
    all_pitstops = get_all_pitstops()
    
    print('Obteniendo información de los conductores... ')
    salida = get_drivers(all_pitstops)
    drivers_df = salida[0]
    pilotos_retirados = salida[1]
    
    print('Creando mapeo id-numero... ')
    mapeo_df = get_mapeo(drivers_df,pilotos_retirados)
    
    print('Generando dataframes por carrera...  ')
    races_dataframes = get_all_races_dataframes(all_pitstops,mapeo_df)
    
    print('Guardando dataframes en csv... ')
    guardar(races_dataframes,all_pitstops)
    print('Proceso de obtención de pitstops finalizado.')