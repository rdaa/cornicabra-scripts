#Recorre una carpeta de archivos Geojson generados por ogr2ogr y los reformatea para introducirlos en 
#la base de datos de cornicabra. 
#Obvia varios datos y añade otros (las bounding boxes) y el formato de los documentos resultantes es:
#{
# "provincia":
# "municipio":
# "agregado":
# "zona":
# "poligono":
# "parcela":
# "recinto":
# "uso_sigpac":
# "bbox":
# "bbox_tiles":
# "dn_surface":
# "geometria":
#}


import json
import os
import math

carpeta = "geopackage/19"
json_string = ""

def bbox(poligono):
    min_lon = float('inf')
    min_lat = float('inf')
    max_lon = float('-inf')
    max_lat = float('-inf')
    for coordenada in poligono["coordinates"][0]:
            lon, lat = coordenada
            min_lon = min(min_lon, lon)
            min_lat = min(min_lat, lat)
            max_lon = max(max_lon, lon)
            max_lat = max(max_lat, lat)
    return [(min_lon, min_lat), (max_lon, max_lat)]

def lonlat2tile(lon,lat,zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def bbox_tiles(bbox_r):
    bbox_t = []
    for punto in bbox_r:
        bbox_t.append(lonlat2tile(punto[0], punto[1], 18))
    return bbox_t
        

print(len(os.listdir(carpeta)))
archivo = os.listdir(carpeta)[0]
for archivo in os.listdir(carpeta):
    with open(os.path.join(carpeta,archivo),"r") as f:
        print("Cargando ", archivo)
        datos = json.load(f)
        f.close()
    recintos = datos["features"]
    json_string = ""
    print("Formateando...")
    for (i,r) in enumerate(recintos):
            # print("polígono:", r["properties"]["poligono"])
            # print("parcela: ", r["properties"]["parcela"])
            bbox_lonlat = bbox(r["geometry"])
            bbox_t = bbox_tiles(bbox_lonlat)
            recinto_formato_nuevo = {
                "provincia":r["properties"]["provincia"],
                "municipio":r["properties"]["municipio"],
                "agregado":r["properties"]["agregado"],
                "zona":r["properties"]["zona"],
                "poligono":r["properties"]["poligono"],
                "parcela":r["properties"]["parcela"],
                "recinto":r["properties"]["recinto"],
                "uso_sigpac":r["properties"]["uso_sigpac"],
                "bbox":bbox_lonlat,
                "bbox_tiles":bbox_t,
                "dn_surface":r["properties"]["dn_surface"],
                "geometria":r["geometry"]
            }
            json_string += json.dumps(recinto_formato_nuevo)

                
        
    print("Escribiendo...")
    
    with open(os.path.join(carpeta,archivo), "w") as f:
        f.write(json_string)
        f.close