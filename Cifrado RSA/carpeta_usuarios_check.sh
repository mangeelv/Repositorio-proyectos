#!/bin/bash

# Script que comprueba la existencia de y crea o no la carpeta 'Usuarios'

directorio="Usuarios"
if ! [ -d $directorio ]; then
    mkdir "$directorio"
fi

