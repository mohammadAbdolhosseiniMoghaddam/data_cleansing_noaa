# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:02:55 2018

@author: mohammad
"""


from lat_long_position import points
import pandas as pd
station_info=pd.read_csv("rstations.csv")
Distance=pd.DataFrame(data=None,index=station_info["station"],columns=station_info["station"])
position=pd.DataFrame(data=None,index=station_info["station"],columns=station_info["station"])
for index_1,i in station_info.iterrows():
    for index_2,j in station_info.iterrows():
       Distance.loc[str(i["station"]),str(j["station"])]=points([i["latitude"],i["longitude"]],
                    [j["latitude"],j["longitude"]]).get_distance()
       position.loc[str(i["station"]),str(j["station"])]=points([i["latitude"],i["longitude"]],
                    [j["latitude"],j["longitude"]]).get_position()
      
