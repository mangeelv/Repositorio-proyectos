import funciones as f 
import pymysql


leer_datos = 1
user = "mangel"
password = "Nukanacioenel2016!"
host = 'localhost'
connection_mysql = pymysql.connect(
    host = host,
    user = user,
    password=password
)
nombre_base_datos = 'Lastfm'
with connection_mysql:
    cursor = connection_mysql.cursor()
    sql = 'CREATE DATABASE ' +  str(nombre_base_datos)
    cursor.execute(sql)
    sql = 'SHOW DATABASES'
    cursor.execute(sql)
    cursor.close()
if __name__ == '__main__':
    if leer_datos:
        print('Leyendo ficheros... ')
        datos = f.leer_ficheros()
        df1 = datos[0]
        df2 = datos[1]
        print('Información sin procesar: ')
        f.mostrar_informacion(df1,df2)
        print('Procesando datos... ')
        datos = f.limpiar_dataframes(df1,df2)
        df1 = datos[0]
        df2 = datos[1]
        print('Información procesada: ')
        f.mostrar_informacion(df1,df2)
        print('Creando tablas... ')
        f.crear_tablas(df1,df2)

    print('Creando base de datos... ')
    f.crear_base_de_datos(user,password,host)
    print('Base de datos creada')

    