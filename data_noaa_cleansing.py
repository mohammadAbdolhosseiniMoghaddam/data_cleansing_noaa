# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:44:07 2018

@author: mohammad
"""

import pandas as pd
#import numpy
city = "la_"
importing_file = "1192617.csv"
station_NAME = "LOSANGELES_DOWNTOWN_USC"
file_name = "MET_"+city+station_NAME+".csv"
site_num ="60371103"



cols = ["STATION", "STATION_NAME", "ELEVATION", "LATITUDE", "LONGITUDE", "DATE", "HOURLYVISIBILITY",
        "HOURLYDRYBULBTEMPC", "HOURLYWETBULBTEMPC", "HOURLYDewPointTempC", "HOURLYRelativeHumidity", "HOURLYWindSpeed", "HOURLYWindDirection", "HOURLYStationPressure", "HOURLYPrecip"]
# col_dtype={'DATE"}
col_dtype = {"DATE": str, "HOURLYVISIBILITY": str}

df = pd.read_csv(importing_file, usecols=cols, dtype=col_dtype, index_col=False)

for i in cols:
    df[i] = df[i].replace(to_replace={"HOURLYPrecip": {'T': 0}})
    df[i] = df[i].map(lambda x: str(x).rstrip('aABbCcDdEeFfgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVxXyYzZ'))
    df[i] = df[i].str.replace('*', '')
   # df.insert(5,'site_name',site_num)


df.insert(13, 'siteP_milibar', pd.to_numeric(df["HOURLYStationPressure"], errors='coerce')*33.8639)
df.insert(5, "site_pm", str(site_num))


df.to_csv(file_name)
