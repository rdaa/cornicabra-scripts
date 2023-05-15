# Script que elimina la linea 1 de los archivos geojson obtenidos tras la exportación
# generada por ogr2ogr. ("FeatureCollection")
# En desuso, usar cambiar_formato_json_recintos.py


import os



carpeta = "geopackage/19"

for archivo in os.listdir(carpeta):
    
    with open(os.path.join(carpeta,archivo), 'r') as archivo_old:

        lineas = archivo_old.readlines()
        print(archivo)
        lineas.pop(1)
        
        archivo_old.close()

    with open(os.path.join(carpeta,archivo), 'w') as archivo_new:
        archivo_new.writelines(lineas)
        archivo_new.close()
