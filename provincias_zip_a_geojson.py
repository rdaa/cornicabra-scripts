#Script que extrae una carpeta de archivos zip

import zipfile
import os
carpeta_zip = "19"
carpeta_geopackage = "geopackage/19"

for archivo in os.listdir(carpeta_zip):
    with zipfile.ZipFile(os.path.join(carpeta_zip,archivo), 'r') as zip_ref:
        try:
            zip_ref.extractall(carpeta_geopackage)
        except:
            print("Error ", os.path.join(carpeta_zip,archivo))