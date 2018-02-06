# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 16:42:59 2018
@author: mohammad moghaddam
Description: Calculating the relative positions given Lat and Long of two points
NE:North East, E:East, W:west, SE: South East, N:North, S:South
NAN:the same point
Input= csv file with corresponding columns named station, latitude, longitude
Output= csv file with two sheets. column relative to rows( read row then column if it was e, it mneans that column located at the east)
"""
from math import sin, cos, sqrt,atan2,radians,degrees
import pandas as pd

"""
Define the class for two points
"""
class points:
    def __init__( self, A, B ):
        self._latA= radians(A[0])
        self._longA= radians(A[1])
        self._latB= radians(B[0])
        self._longB= radians(B[1])
        self._dlon= self._longB-self._longA
        self._dlat= self._latB-self._latA
    def get_distance(self):    # get distance between two points
        a = (sin(self._dlat/2))**2 + cos(self._latB) * cos(self._latA) * (sin(self._dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = 6373.0 * c
        return distance
    def get_position(self):  # get the relative position to A
        degree=degrees(atan2(self._dlat,self._dlon))
        if degree==0:
            pos="NAN"
        elif -15<degree<15:
            pos="E"
        elif 15<degree<75:
            pos="NE"
        elif 75<degree<105:
            pos="N"
        elif 105<= degree<165:
            pos="NW"
        elif -75<= degree< -15:
            pos="SE"
        elif -105<= degree<-75:
            pos="S"
        elif -165<= degree<-105:
            pos="SW"
        else:
            pos="W"
        return pos

"""
Make two spreadsheets to find the reative position and distance of points
"""
def position_matrix(input_file):
    station_info=pd.read_csv(input_file)
    Distance=pd.DataFrame(data=None,index=station_info["station"],columns=station_info["station"])
    position=pd.DataFrame(data=None,index=station_info["station"],columns=station_info["station"])
    for index_1,i in station_info.iterrows():     #iteration in dataframe
        for index_2,j in station_info.iterrows():
           Distance.loc[str(i["station"]),str(j["station"])]=points([i["latitude"],i["longitude"]],
                        [j["latitude"],j["longitude"]]).get_distance()
           position.loc[str(i["station"]),str(j["station"])]=points([i["latitude"],i["longitude"]],
                        [j["latitude"],j["longitude"]]).get_position()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('geographic_position.xlsx', engine='xlsxwriter')
    Distance.to_excel(writer,sheet_name="Distance")
    position.to_excel(writer,sheet_name="position")
    writer.save()
    return Distance,position

"""
position_locator(st,df): given a site name, return the position of other sites 
st: name of station
df_position: matrix of relative position between two points
df_distance: matrix of distance
lower_bad,uper_band: the distance ranges
output: a dictionary with directions as keys and tuples of dist and sitnum as values
"""
def position_locator(st,df_position,df_distance,lower_bad=5,uper_band=60):
        Directions=["E","NE","N","NW","SE","S","SW","W"]
        dic_pos_dist={}
        for i in Directions:
            station_dist=df_distance.loc[str(st),
                                             df_position.loc[str(st),]==i]
            station_dist=station_dist[station_dist.between(lower_bad,uper_band)]
            station_dist.sort_values(inplace=True) # sort based on distance
            if len( station_dist )==0:
                dic_pos_dist[i]="N/A"  
            else:
               dic_pos_dist[i]=list(zip(station_dist.index,station_dist)) 
        return dic_pos_dist

"""
Run an example:
"""
input_file="rstations.csv"
dis,pos=position_matrix(input_file)
stationum="google_6012"
df=position_locator(stationum,pos,dis)
#pd.DataFrame(df)
print(position_locator(stationum,pos,dis))
pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in df.items() ]))
#station_dist=dis.loc[str(stationum),pos.loc[str(stationum),]==i]

