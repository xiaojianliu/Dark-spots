# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 12:48:38 2016
settting time different and distance between 2 drifter start point get pair of drifter one 
is drogue drifter another is surface drifter
get the picture of pair of drifter's track 
@author: xiaojian
"""
import sys
import datetime as dt
from matplotlib.path import Path
import netCDF4
from dateutil.parser import parse
import numpy as np
import math
import pandas as pd
from datetime import datetime, timedelta
from math import radians, cos, sin, atan, sqrt  
from matplotlib.dates import date2num,num2date
import matplotlib.pyplot as plt
import csv
from drifter_vs_model_function import drifterhr
####hard code
time_different=0.02#1hour
dis=1
depth_different=5
######function
def haversine(lon1, lat1, lon2, lat2): 
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """   
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
    #print 34
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * atan(sqrt(a)/sqrt(1-a))   
    r = 6371 
    d=c * r
    #print type(d)
    return d
def get_drifter_erddap(id,start_time,days):
    """
     get data from url, return ids latitude,longitude, times
     input_time can either contain two values: start_time & end_time OR one value:interval_days
     and they should be timezone aware
     example: input_time=[dt(2012,1,1,0,0,0,0,pytz.UTC),dt(2012,2,1,0,0,0,0,pytz.UTC)]
     """
    df=dict(id=[],lon=[],lat=[],time=[])
    #mintime=start_time.strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')  # change time format
    endtime=datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')+timedelta(days)    
    maxtime=endtime.strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')    
    # open url to get data
    #url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id,time,latitude,longitude&id=%22100390731%22&time>='+str(mintime)+'&time<='+str(maxtime)+'&orderBy(%22time%22)'
    url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id,time,latitude,longitude&time>='\
    +str(start_time)+'&time<='+str(maxtime)+'&id="'+str(id)+'"&orderBy("time")'
    df=pd.read_csv(url,skiprows=[1])
    for k in range(len(df)):
        df.time[k]=parse(df.time[k][:-1])
    df=df[df.longitude <=-20]
    return df.time.values,df.latitude.values,df.longitude.values    
def get_drifter_track(start_time, days,drifter_ID): 
    """
     the fuction use the function of get_drifter_erddap get drifter point
     the drifter point include ids,lat_hr,lon_hr,lon,lat,time,distance
     
     """
    dr_points=dict(lon=[],lat=[],time=[]) 
    drpoints=dict(ids=[],lat_hr=[],lon_hr=[],lon=[],lat=[],time=[],distance=[])
    drifter_points = dict(lon=[],lat=[],time=[])
    dr_point=dict(lon=[],lat=[],time=[]) 
    drtime=[]
    id=drifter_ID
    ids=id
    dr_point['time'],dr_point['lat'],dr_point['lon'] =get_drifter_erddap(id,start_time,days+1)     
    for w in range(len(dr_point['time'])):       
        times=[]       
        times=dr_point['time'][w].replace(tzinfo=None)
        time=times-timedelta(hours=4)
        drtime.append(time)  
    drtimenp = np.array(drtime)
    dst = drtimenp-datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
    dstindex = np.argmin(abs(dst))
    det = drtimenp-(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')+timedelta(days))
    detindex = np.argmin(abs(det))#every compare days drifter end index
    dr_points['lon']=dr_point['lon'][dstindex:detindex]
    dr_points['lat']=dr_point['lat'][dstindex:detindex]
    drifter_points['time']=drtime[dstindex:detindex]   
    dr_points['lon'].tolist
    dr_points['lat'].tolist

    drpoints=dr_points ;
    drpoints['ids']=ids;
    drpoints['time']=drifter_points['time']
    return drpoints
    
### program starts
####get ids
url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id'
df=pd.read_csv(url,skiprows=[1])
id_all=df.id.values
ids = []
for id in id_all:
    if id not in ids:
        ids.append(id)
#### define the different paramenters
file_data=[]#two initial position closer to drifter the different data
fileids=[]#two initial position closer to drifter the different id
filetime=[]#two initial position closer to drifter the different time
filelon=[]#two initial position closer to drifter the different longitude
filelat=[]#two initial position closer to drifter the different latitude
filedeep=[]#two initial position closer to drifter the different depth
start_times=[]#the beginning of a different id start time
depths=[]#the beginning of a different id depths
lons=[]#the beginning of a different id longitude
lats=[]#the beginning of a different id latitude
length=[]#time length
time=[]
result=dict(id=[],dis=[],mintimedis=[],maxtimedis=[],meantimedis=[],mindisdis1=[],maxdisdis1=[],meandisdis1=[],mindisdis2=[],maxdisdis2=[],meandisdis2=[])
### differet id start value obtained
for i in range(len(ids)):
    url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id,time,latitude,longitude,depth&id=%22'+str(ids[i])+'%22&orderBy(%22time%22)'
    df=pd.read_csv(url,skiprows=[1])
    start_times.append(df.time.values[0])
    time.append(df.time.values)
    length.append(date2num(datetime.strptime(df.time.values[-1], '%Y-%m-%dT%H:%M:%SZ'))-date2num(datetime.strptime(df.time.values[0], '%Y-%m-%dT%H:%M:%SZ')))
    depths.append(df.depth.values[0])
    lons.append(df.longitude.values[0])
    lats.append(df.latitude.values[0]);
### the output image 
for i in range(len(ids)):
    for o in range(i,len(ids)):
        if i!=o:
            
            time_period=date2num(datetime.strptime(start_times[i], '%Y-%m-%dT%H:%M:%SZ'))-date2num(datetime.strptime(start_times[o], '%Y-%m-%dT%H:%M:%SZ'))
            distance=haversine(lons[i],lats[i],lons[o],lats[o])
            
            if abs(time_period)<time_different and abs(distance)<dis and abs(abs(depths[o])-abs(depths[i]))>=depth_different and length[i]>1 and length[o]>1 :
                
                filedeep.extend((depths[o],depths[i]))
                fileids.extend((ids[o],ids[i]))
                ii=[]
                ii=str(str(ids[i])+'vs'+str(ids[o]))
                result['id'].append(ii)
                if (date2num(datetime.strptime(start_times[i], '%Y-%m-%dT%H:%M:%SZ'))-date2num(datetime.strptime(start_times[o], '%Y-%m-%dT%H:%M:%SZ')))>0:
                    filetime.append(str(start_times[i]))
                else:
                    filetime.append(str(start_times[o]))
                filelat.extend((lons[o],lons[i]))
                filelon.extend((lats[o],lats[i]))
                
                drifter_points1=dict(ids=[],lat_hr=[],h_hr=[],lon_hr=[],lon=[],lat=[],time=[],distance=[],wdistance=[])
                drifter_points2=dict(ids=[],lat_hr=[],h_hr=[],lon_hr=[],lon=[],lat=[],time=[],distance=[],wdistance=[])            
                drifter_points_1=get_drifter_track(start_times[i],3,ids[i])
                drifter_points1['ids']=ids[i]
                drifter_points1['lon']=(drifter_points_1['lon'])
                drifter_points1['lat']=(drifter_points_1['lat'])
                
                
                drifter_points_2=get_drifter_track(start_times[o],3,ids[o])
                drifter_points2['ids']=ids[0]
                drifter_points2['lon']=(drifter_points_2['lon'])
                drifter_points2['lat']=(drifter_points_2['lat'])
                for aa in range(min(len(drifter_points_1['time']),len(drifter_points_2['time']))):
                    if (drifter_points_1['time'][aa]-drifter_points_2['time'][aa]).days*24*3600+(drifter_points_1['time'][aa]-drifter_points_2['time'][aa]).seconds>0:
                        
                        drifter_points1['time'].append(drifter_points_1['time'][aa])
                        drifter_points2['time'].append(drifter_points_1['time'][aa])
                    else:
                        drifter_points1['time'].append(drifter_points_2['time'][aa])
                        drifter_points2['time'].append(drifter_points_2['time'][aa])
                a=(drifter_points1['time'][-1]-drifter_points1['time'][0]).days+math.floor(((drifter_points1['time'][-1]-drifter_points1['time'][0]).seconds)/3600.0)/24.0
                drifter_points1=drifterhr(drifter_points1,a)
                drifter_points2=drifterhr(drifter_points2,a)
                
                if len(drifter_points_1['lon'])!=0 and len(drifter_points_2['lon'])!=0:
                    plt.figure(1)
                    plt.plot(drifter_points_1['lon'],drifter_points_1['lat'],'bo-',label='drifter %s and deep %s m'%(ids[i],-abs(depths[i])))
                    plt.plot(drifter_points_2['lon'],drifter_points_2['lat'],'ro-',label='drifter %s and deep %s m'%(ids[o],-abs(depths[o])))
                    plt.legend()
                    plt.grid(True)
                    plt.title('drifter %s and %s track ' %(ids[o],ids[i]))
                    plt.savefig('drifter %s and %s track ' %(ids[o],ids[i]))
                    plt.show()
                distances=[]
                disone=[]
                distwo=[]
                timedis=[]
                disdis1=[]
                disdis2=[]
                diss=[]
                for bb in range(len(drifter_points1['lon_hr'])):
                    distances.append(haversine(drifter_points1['lon_hr'][bb],drifter_points1['lat_hr'][bb],drifter_points2['lon_hr'][bb],drifter_points2['lat_hr'][bb]))
                plt.figure(2)
                plt.plot(distances[:])
                plt.ylabel('distance(km)') 
                plt.xlabel('time(hour)')
                plt.title('drifter %s and %s distance ' %(ids[o],ids[i]))
                plt.savefig('drifter %s and %s distance ' %(ids[o],ids[i]))
                plt.show()
                for cc in range(1,len(drifter_points1['lon_hr'])):
                    disone.append(haversine(drifter_points1['lon_hr'][0],drifter_points1['lat_hr'][0],drifter_points1['lon_hr'][cc],drifter_points1['lat_hr'][cc]))
                    distwo.append(haversine(drifter_points2['lon_hr'][0],drifter_points2['lat_hr'][0],drifter_points2['lon_hr'][cc],drifter_points2['lat_hr'][cc]))
                result['dis'].append(distances)
                for dd in range(1,len(distances)):
                    diss.append(distances[dd]-distances[0])
                    timedis.append((distances[dd]-distances[0])/dd) 
                result['meantimedis'].append(np.mean(timedis))
                result['mintimedis'].append(np.min(timedis))
                result['maxtimedis'].append(np.max(timedis))
                for ee in range(len(diss)):
                    disdis1.append(diss[ee]/disone[ee])
                    disdis2.append(diss[ee]/distwo[ee])
                result['mindisdis1'].append(np.min(disdis1))
                result['maxdisdis1'].append(np.max(disdis1))
                result['meandisdis1'].append(np.mean(disdis1))
                
                result['mindisdis2'].append(np.min(disdis2))
                result['maxdisdis2'].append(np.max(disdis2))
                result['meandisdis2'].append(np.mean(disdis2))
                
#print file              
file_data.append(fileids)
file_data.append(filetime)
file_data.append(filelon)
file_data.append(filelat)
file_data.append(filedeep)
aa=(len(file_data[0]))
i=0
j=1
id1=[]
id2=[]
lon1=[]
lat1=[]
lon2=[]
lat2=[]
deep1=[]
deep2=[]
datab=[]
while i<=aa-2:
    it=file_data[0][i]
    id1.append(it)
    itt=file_data[2][i]
    lon1.append(itt)
    ittt=file_data[3][i]
    lat1.append(ittt)
    itttt=-abs(file_data[4][i])
    deep1.append(itttt)
    i+=2
while j<=aa-1:
    it=file_data[0][j]
    id2.append(it)
    itt=file_data[2][j]
    lon2.append(itt)
    ittt=file_data[3][j]
    lat2.append(ittt)
    itttt=-abs(file_data[4][j])
    deep2.append(itttt)
    j+=2

datab.append(file_data[1])
datab.append(result['id'])
datab.append(result['mintimedis'])
datab.append(result['maxtimedis'])
datab.append(result['meantimedis'])
datab.append(id1)  
datab.append(lon1) 
datab.append(lat1)
datab.append(deep1)
datab.append(result['mindisdis1'])
datab.append(result['maxdisdis1'])
datab.append(result['meandisdis1'])
datab.append(id2)  
datab.append(lon2) 
datab.append(lat2)
datab.append(deep2)
datab.append(result['mindisdis2'])
datab.append(result['maxdisdis2'])
datab.append(result['meandisdis2'])
  
dr=map(list, zip(*datab))
csvfile = file('deep_vs_surface.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['time', 'id1_vs_id2','min(distance/hour) km/h','max(distance/hour) km/h','mean(distance/hour) km/h',\
 'id1','start_lon1','start_lat1','deep1','min(dis/dis) km/km','max(dis/dis) km/km','mean(dis/dis) km/km',\
 'id2', 'start lon2','start lat2','deep2','min(dis/dis) km/km','max(dis/dis) km/km','mean(dis/dis) km/km'])
writer.writerows(dr)
csvfile.close() 
