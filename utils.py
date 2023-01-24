from pyproj import Geod
from shapely.ops import cascaded_union
from shapely.geometry import Polygon,mapping
from h3 import h3
import pandas as pd
import numpy as np
from numpy import concatenate

geod = Geod(ellps="WGS84")
RANDOM_STATE = 1997

def bbox_to_h3(geometry,resolution):
# All the points should be follow longitude latitide order
    hexas = h3.polyfill({
                    'type':'Polygon',
                    "coordinates": [[geometry[0],geometry[1],geometry[2],geometry[3],geometry[0]]]},res=resolution,geo_json_conformant=True)
    return list(set(hexas))

def polygon_to_h3(polygon,resolution):
    polygon = mapping(polygon)
    hexas = h3.polyfill(polygon,res=resolution,geo_json_conformant=True)
    return list(set(hexas))

def add_h3_cell(df,resolution):
    '''Add hexagon cell id for given dataframe'''
    df['h3'] = df.apply(lambda x: h3.geo_to_h3(x['lat'],x['lng'],resolution=resolution),axis=1)
    return df

def dict_to_shapely(d):
    coords = d['features'][0]['geometry']['coordinates'][0]
    return Polygon(coords)

def generate_random_dataset(lat_lons,poi_categories,N=None):
    if isinstance(lat_lons,list):
        lat_lons = np.array(lat_lons)
        
    df = pd.DataFrame(columns=['latitude','longitude','category'])
    
    for category in poi_categories:
        if N is None:
            n = np.random.randint(low=10,high=30)
        else:
            n = N
        idx = np.random.choice(range(len(lat_lons)),size=n,replace=False)
        tmp_df = pd.DataFrame(lat_lons[idx,:],columns=['latitude','longitude']) 
        tmp_df['category'] = category
        df = pd.concat([df,tmp_df])
    return df.sample(frac=1).reset_index(drop=True)
