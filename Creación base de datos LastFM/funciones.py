import pandas as pd
from datetime import datetime
import pymysql
import csv





def leer_csv(nombre_archivo):
    '''Lee un csv y devuelve una lista de tuplas'''
    lista_tuplas = []
    with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            fila = [None if elemento == '' else elemento for elemento in fila] # Este paso es crucial
            tupla = tuple(fila)
            lista_tuplas.append(tupla)
    return lista_tuplas[1:]

def leer_ficheros():
    numero_de_filas = 2000000
    df1 = pd.read_csv('userid-profile.tsv', sep='\t',nrows=numero_de_filas)
    nombres_columnas = ['userid','timestamp','artid','artname','traid','traname']
    df2 = pd.read_csv('userid-timestamp-artid-artname-traid-traname.tsv', sep='\t',error_bad_lines=False,header=None, names=nombres_columnas,nrows=numero_de_filas)

    return df1, df2

def mostrar_informacion(df1,df2):
    print('DF1')
    print(df1.head())
    print(df1.info())
    print('\n')
    print('DF2')
    print(df2.head())
    print(df2.info())

def limpiar_dataframes(df1,df2):
    df2 = df2.dropna(subset='traid')
    df2 = df2.head(1000000)

    df2['timestamp'] = pd.to_datetime(df2['timestamp'], format="%Y-%m-%dT%H:%M:%SZ").dt.strftime("%Y-%m-%d %H:%M:%S")
    df1['registered'] = df1['registered'].apply(lambda x: datetime.strptime(x, "%b %d, %Y").strftime("%Y-%m-%d %H:%M:%S") if pd.notna(x) else pd.NaT)
    df1['internuserid'] = df1['#id'].str.lstrip('user_').str.lstrip('0')
    df2['internuserid'] = df2['userid'].str.lstrip('user_').str.lstrip('0')
   

    
    df2['interntraid'] = df2['traid'].factorize()[0] + 1
    df2['internartid'] = df2['artid'].factorize()[0] + 1
    df1['interncountryid'] = df1['country'].factorize()[0] + 1
    # factorize se utiliza para asignar un número entero único a cada valor único en las columnas 'traid', 'artid' y 'country'
    df1.where(pd.notna(df1), None)
    df2.where(pd.notna(df2), None)
        

    return df1, df2

def crear_tablas(df1,df2):
    '''Crea archivos csv con las tablas de la futura base de datos'''
    tablas = {'artistas':None,'canciones':None,'usuarios':None,'paises':None,'escuchas':None}


    # Tabla de escuchas 
    tablas['escuchas'] = df2[['internuserid','interntraid','internartid','timestamp']].reset_index(drop=True)
    tablas['escuchas']['index'] = tablas['escuchas'].index # esta será nuestra clave primaria 
    print(tablas['escuchas'].head())
    print(tablas['escuchas'].info())

    # Tabla de artistas 
    tablas['artistas'] = df2[['internartid','artid','artname']].reset_index(drop=True).drop_duplicates(subset='internartid')
    print(tablas['artistas'].head())
    print(tablas['artistas'].info())

    # Tabla de canciones 
    tablas['canciones'] = df2[['interntraid','traid','traname']].reset_index(drop=True).drop_duplicates(subset='interntraid')
    print(tablas['canciones'].head())
    print(tablas['canciones'].info())

    # Tabla de usuarios 
    tablas['usuarios'] = df1[['internuserid','#id','gender','age','interncountryid','registered']].reset_index(drop=True).drop_duplicates(subset='internuserid')
    print(tablas['usuarios'].head())
    print(tablas['usuarios'].info())

    # Tabla de países
    tablas['paises'] = df1[['interncountryid','country']].reset_index(drop=True).drop_duplicates(subset='interncountryid')
    print(tablas['paises'].head())
    print(tablas['paises'].info())

    for clave,valor in tablas.items():
        valor.to_csv(f'{clave}.csv', index=False)


def crear_base_de_datos(user:str,password:str,host:str):
        '''Introduce todas las tablas en la base Lastfm, definiendo claves primarias y foráneas'''
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database='Lastfm'
        )
 
        cursor = connection.cursor()

        # Tabla países 
        valores_a_insertar = leer_csv('paises.csv')
        sql = '''
            CREATE TABLE paises (
            interncountryid INT PRIMARY KEY,
            country VARCHAR(50) 
            );'''
        cursor.execute(sql)
        sql = '''
        INSERT INTO paises (interncountryid,  country)
        VALUES(%s,%s);'''
        cursor.executemany(sql,valores_a_insertar)
        connection.commit()

        # Tabla usuarios
        valores_a_insertar = leer_csv('usuarios.csv')
        sql = '''CREATE TABLE usuarios (
        internuserid INT PRIMARY KEY,
        userid VARCHAR(100),
        gender VARCHAR(100),
        age FLOAT,
        interncountryid INT, 
        registered DATETIME,
        FOREIGN KEY (interncountryid) REFERENCES paises(interncountryid)
        )'''
        cursor.execute(sql)
        sql = '''
        INSERT INTO usuarios (internuserid, userid, gender, age, interncountryid, registered)
        VALUES(%s,%s,%s,%s,%s,%s);
        '''
        cursor.executemany(sql,valores_a_insertar)
        connection.commit()

        # Tabla canciones
        valores_a_insertar = leer_csv('canciones.csv')
        sql = '''CREATE TABLE canciones (
        interntraid INT PRIMARY KEY,
        traid VARCHAR(100),
        traname VARCHAR(500)
        )'''
        cursor.execute(sql)
        sql = '''
        INSERT INTO canciones (interntraid, traid, traname)
        VALUES(%s,%s,%s);
        '''
        cursor.executemany(sql,valores_a_insertar)
        connection.commit()

        # Tabla artistas
        valores_a_insertar = leer_csv('artistas.csv')
        sql = '''CREATE TABLE artistas (
        internartid INT PRIMARY KEY,
        artid VARCHAR(100),
        artname VARCHAR(100)
        )'''
        cursor.execute(sql)
        sql = '''
        INSERT INTO artistas (internartid, artid,artname)
        VALUES(%s,%s,%s);
        '''
        cursor.executemany(sql,valores_a_insertar)
        connection.commit()

        # Tabla escuchas 
        valores_a_insertar = leer_csv('escuchas.csv')
        sql = '''
            CREATE TABLE escuchas (
            internuserid INT,
            interntraid INT,
            internartid INT, 
            timestamp DATETIME, 
            indice INT PRIMARY KEY,
            FOREIGN KEY (internuserid) REFERENCES usuarios(internuserid),
            FOREIGN KEY (interntraid) REFERENCES canciones(interntraid),
            FOREIGN KEY (internartid) REFERENCES artistas(internartid)
           )'''
        cursor.execute(sql)
        sql = '''
        INSERT INTO escuchas (internuserid, interntraid, internartid, timestamp, indice)
        VALUES(%s,%s,%s,%s,%s)'''
        cursor.executemany(sql,valores_a_insertar)
        connection.commit()

        cursor.close()
  
