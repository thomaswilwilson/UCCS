import pandas as pd
from sympy import Point
from sympy.geometry import Segment, intersection
#import geopandas as gpd
import shapely.ops
from shapely import wkt
from shapely.geometry import Point as ShP
from shapely.geometry import LineString


def intersections(df):
    #sympy
    lines = df.apply(get_line, axis = 1).tolist()
    return intersection(*lines , pairwise=True)
def get_line(row):
    #sympy
    return Segment(Point(row['Pickup Centroid Latitude'],
    row['Pickup Centroid Longitude']), 
    Point(row['Dropoff Centroid Latitude'], 
        row['Dropoff Centroid Longitude']))
def get_ls(row):
    #shapely
    return LineString([wkt.loads(row['pl']),wkt.loads(row['dl'])])
def cleaner(df):
    #shapely
    df2 = df.rename(columns = {'Trip ID' : 'id', 'Pickup Community Area' : 'zone',
       'Pickup Centroid Location' : 'pl', 'Dropoff Centroid Location': 'dl'},
        inplace = True)
    df2 = df.filter(['id','zone', 'pl', 'dl'], axis = 1)
    df2['geometry'] = df2.apply(get_ls, axis = 1)
    return df2.drop(['pl','dl'] ,axis = 1)
def grouped(df):
    new = df.groupby('zone')['line'].agg(lambda x: shapely.ops.linemerge(x.values))
    return gpd.GeoDataFrame(new, geometry = 'geometry').buffer(0.005, resolution = 0)
def get_index(zone_line):
    
