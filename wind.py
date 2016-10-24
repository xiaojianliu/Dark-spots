# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:34:20 2016

@author: hxu
"""

import datetime as dt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import csv
from drifter_vs_model_function import get_drifter_track,get_fvcom,get_roms,calculate_SD,drifterhr
hhhhhhhhh=[]
drifter_data_type='erddap'
Model=['30yr']
drifter_ID =[] 
drifter_list=[]
depth =[-1]
track=30
days=10
track_days=1
restart_days=1
start_times =[dt.datetime(2010,5,19,9,13,0,0)]
wind_get_type='FVCOM'
wind=0.004 
#csvfile = file('drifter_vs_model.csv', 'wb')
#writer = csv.writer(csvfile)
t=0.0
e=0.01
z=(t+e)/2
a1=(t+z)/2
a2=(z+e)/2
c=a2-a1
hahhahahah=''
print 'a1',a1
print 'a2',a2
print 'c',c
while (((c+0.0001)-(a2-a1))<c):
    
    print "get drifter data from "+ drifter_data_type+" use %s model compare %i days" %(Model,days-1)
    if drifter_list==[]:
        if 'ROMS' in Model and '30yr' in Model:
            drifter_list='erddap_drifter_list_both.csv'
        elif 'ROMS' in Model and '30yr' not in Model:
            drifter_list='erddap_drifter_list_roms.csv'
        elif 'ROMS' not in Model and '30yr' in Model:
            drifter_list='erddap_drifter_list_30yr.csv'
    file_drID=[]
    if 'ROMS' in Model:
        romstmeandis=[];romstmindis=[];romstmaxdis=[];romsdmeandis=[];romsdmindis=[];romsdmaxdis=[]
        wromstmeandis=[];wromstmindis=[];wromstmaxdis=[];wromsdmeandis=[];wromsdmindis=[];wromsdmaxdis=[]
    if '30yr' in Model:
        yrtmeandis=[];yrtmindis=[];yrtmaxdis=[];yrdmeandis=[];yrdmindis=[];yrdmaxdis=[]
        wyrtmeandis=[];wyrtmindis=[];wyrtmaxdis=[];wyrdmeandis=[];wyrdmindis=[];wyrdmaxdis=[]
    if 'GOM3' in Model:
        gomtmeandis=[];gomtmindis=[];gomtmaxdis=[];gomdmeandis=[];gomdmindis=[];gomdmaxdis=[]
        wgomtmeandis=[];wgomtmindis=[];wgomtmaxdis=[];wgomdmeandis=[];wgomdmindis=[];wgomdmaxdis=[]
    if 'massbay' in Model:
        masstmeandis=[];masstmindis=[];masstmaxdis=[];massdmeandis=[];massdmindis=[];massdmaxdis=[]
        wmasstmeandis=[];wmasstmindis=[];wmasstmaxdis=[];wmassdmeandis=[];wmassdmindis=[];wmassdmaxdis=[]
    if drifter_ID==[]:  
        start_times=[]    
        drifters = np.genfromtxt(drifter_list,dtype=None,names=['ids','start_time','days','mean','max','min','depth'],delimiter=',',skip_header=1)    
        #print 'length of ids',len(drifters['ids'])
        for i in range(len(drifters['ids'])):
          dt_time=datetime.strptime(drifters['start_time'][i], '%Y-%m-%d'+' '+'%H:%M:%S+00:00')       
          start_times.append(dt_time)
        #print 'start_times',start_times
    else:
        drifters=dict(ids=[],days=[])
        drifters['ids']=drifter_ID
        drifters['depth']=depth
        for b in range(len(drifter_ID)):
            drifters['days'].append(days)
    #print 'drifters',drifters
    
    for num in range(min(len(drifters['ids']),track)): # we limit runs to "track" drifters (typically 20) because it often bombs   
        print 'id=',drifters['ids'][num],'index=',num
        hahhahahah=drifters['ids'][num]
        drifter_points = dict(ids=[],lat_hr=[],h_hr=[],lon_hr=[],lon=[],lat=[],time=[],distance=[],wdistance=[])
        drifter_points['ids']=drifters['ids'][num]
        #print 'drifter_points[ids]',drifter_points['ids']
        if drifters['days'][num]>days:
            drifters['days'][num]=days
        #print 'drifters',drifters
        drifter_points=get_drifter_track(drifter_data_type,start_times[num],drifters['days'][num],drifters['ids'][num]) 
        drifter_points=drifterhr(drifter_points,drifters['days'][num]-1)
        #print 'drifter_points',drifter_points
        
        distance=[]
        wdistance=[]
        meantimedis=[]
        meandisdist=[]
        wmeantimedis=[]
        wmeandisdist=[]
        model_points_s=[]
        wmodel_points_s=[]
        name='distance of driter id=%s'%(drifters['ids'][num])
        csvfile = file(str(name), 'wb')
        writer = csv.writer(csvfile)
        #print 'drifter[days]',drifters['days']
        
        
        
        wmodel_points=dict(lon=[],lat=[],time=[])
        model_points =dict(lon=[],lat=[],time=[])
        
        for nday in np.arange(0,drifters['days'][num]-1,restart_days): 
            #print 'nday',nday
            print 1
            modelpoints = dict(lon=[],lat=[],time=[]) 
            wmodelpoints = dict(lon=[],lat=[],time=[])
            start_time=drifter_points['h_hr'][nday*24]
            end_times=drifter_points['h_hr'][(nday+track_days)*24-1]
            i=Model[0]
            GRIDS= ['GOM3','massbay','30yr']
            if i in GRIDS:
                
                get_obj =  get_fvcom(i)
                url_fvcom = get_obj.get_url(start_time,end_times)                
                b_points = get_obj.get_data(url_fvcom) 
                    
                modelpoints,windspeed= get_obj.get_track(drifter_points['lon_hr'][nday*24],drifter_points['lat_hr'][nday*24],drifters['depth'][num],start_time,a1,wind_get_type)
                wmodelpoints,wwindspeed= get_obj.get_track(drifter_points['lon_hr'][nday*24],drifter_points['lat_hr'][nday*24],drifters['depth'][num],start_time,a2,wind_get_type)
                #print 'modelpoints',modelpoints
            if i=='ROMS':        
                get_obj = get_roms()
                url_roms = get_obj.get_url(start_time,end_times)
                get_obj.get_data(url_roms)
                    
                modelpoints ,windspeed= get_obj.get_track(drifter_points['lon_hr'][nday*24],drifter_points['lat_hr'][nday*24],drifters['depth'][num],start_time,a1,wind_get_type)
                wmodelpoints,wwindspeed= get_obj.get_track(drifter_points['lon_hr'][nday*24],drifter_points['lat_hr'][nday*24],drifters['depth'][num],start_time,a2,wind_get_type)
                    
            model_points['lon'].append(modelpoints['lon']); model_points['lat'].append(modelpoints['lat']);model_points['time'].append(modelpoints['time'])
            wmodel_points['lon'].append(wmodelpoints['lon']); wmodel_points['lat'].append(wmodelpoints['lat']);wmodel_points['time'].append(wmodelpoints['time'])
            dist=[]
            wdist=[]
           
            if len(modelpoints['lon'])==24*track_days:#and windspeed<36:
                
                dist,meantdis,meandisdis=calculate_SD(modelpoints,drifter_points['lon_hr'][nday*24:(nday+track_days)*24],drifter_points['lat_hr'][nday*24:(nday+track_days)*24],drifter_points['h_hr'][nday*24:(nday+track_days)*24])
                wdist,wmeantdis,wmeandisdis=calculate_SD(wmodelpoints,drifter_points['lon_hr'][nday*24:(nday+track_days)*24],drifter_points['lat_hr'][nday*24:(nday+track_days)*24],drifter_points['h_hr'][nday*24:(nday+track_days)*24])
            else:
                continue
                dist,meantdis,meandisdis=calculate_SD(modelpoints,drifter_points['lon_hr'][nday*24:(nday+track_days)*24],drifter_points['lat_hr'][nday*24:(nday+track_days)*24],drifter_points['h_hr'][nday*24:(nday+track_days)*24])
                wdist,wmeantdis,wmeandisdis=calculate_SD(wmodelpoints,drifter_points['lon_hr'][nday*24:(nday+track_days)*24],drifter_points['lat_hr'][nday*24:(nday+track_days)*24],drifter_points['h_hr'][nday*24:(nday+track_days)*24])
            #print 'dist',dist
            distance.append(dist)#one drifter one model all distance 
            #print 'distance',distance
            meandisdist.append(meandisdis) #one drifter one model per day mean distance/dist                
            meantimedis.append(meantdis)#one drifter one model per day mean distance/day
                    
            wdistance.append(wdist) 
            wmeandisdist.append(wmeandisdis)                
            wmeantimedis.append(wmeantdis)
            #writer.writerow(fh)
            
            #plt.figure(2)
            #plt.title('id=%s drifter day=%s  vs modle=%s distance'%(drifters['ids'][num],drifter_points['h_hr'][nday*24],Model[0]))
            #plt.plot(dist[:],'b-')
            #plt.plot(wdist[:],'b-')
            #plt.ylabel('distance(km)')   
            #plt.xlabel('time')  
            #plt.savefig('id=%s drifter day=%s  vs modle=%s distance'%(drifters['ids'][num],drifter_points['h_hr'][nday*24],Model[0]))
            #plt.show()
        

        #print 'model_points',model_points
        #plt.figure(1) 
        #plt.title('id=%s drifter track vs modle=%s'%(drifters['ids'][num],Model[0]))
        #for haha in np.arange(0,drifters['days'][num]-1,restart_days): 
            #plt.plot(model_points['lon'][haha],model_points['lat'][haha],'ro-')
            #plt.plot(wmodel_points['lon'][haha],wmodel_points['lat'][haha],'yo-')
        
        #plt.plot(drifter_points['lon'][0:],drifter_points['lat'][0:],'bo-')
        #plt.grid(True)
        #plt.savefig('id=%s drifter track vs modle=%s'%(drifters['ids'][num],Model[0]))  
        #plt.show()
        if Model[0] == 'ROMS':
            wromstmeandis.append(np.mean(wmeantimedis))
            wromstmindis.append(min(wmeantimedis))
            wromstmaxdis.append(max(wmeantimedis))
            wromsdmeandis.append(np.mean(wmeandisdist))
            wromsdmindis.append(min(wmeandisdist))
            wromsdmaxdis.append(max(wmeandisdist))
            
            romstmeandis.append(np.mean(meantimedis))
            romstmindis.append(min(meantimedis))
            romstmaxdis.append(max(meantimedis))
            romsdmeandis.append(np.mean(meandisdist))
            romsdmindis.append(min(meandisdist))
            romsdmaxdis.append(max(meandisdist))
        if Model[0] == '30yr':
            yrtmeandis.append(np.mean(meantimedis))
            yrtmindis.append(min(meantimedis))
            yrtmaxdis.append(max(meantimedis))
            yrdmeandis.append(np.mean(meandisdist))
            yrdmindis.append(min(meandisdist))
            yrdmaxdis.append(max(meandisdist))
            
            wyrtmeandis.append(np.mean(wmeantimedis))
            wyrtmindis.append(min(wmeantimedis))
            wyrtmaxdis.append(max(wmeantimedis))
            wyrdmeandis.append(np.mean(wmeandisdist))
            wyrdmindis.append(min(wmeandisdist))
            wyrdmaxdis.append(max(wmeandisdist))
        if Model[0] == 'GOM3':
            gomtmeandis.append(np.mean(meantimedis))
            gomtmindis.append(min(meantimedis))
            gomtmaxdis.append(max(meantimedis))
            gomdmeandis.append(np.mean(meandisdist))
            gomdmindis.append(min(meandisdist))
            gomdmaxdis.append(max(meandisdist))
            
            wgomtmeandis.append(np.mean(wmeantimedis))
            wgomtmindis.append(min(wmeantimedis))
            wgomtmaxdis.append(max(wmeantimedis))
            wgomdmeandis.append(np.mean(wmeandisdist))
            wgomdmindis.append(min(wmeandisdist))
            wgomdmaxdis.append(max(wmeandisdist))
        if Model[0] == 'massbay':
            masstmeandis.append(np.mean(meantimedis))
            masstmindis.append(min(meantimedis))
            masstmaxdis.append(max(meantimedis))
            massdmeandis.append(np.mean(meandisdist))
            massdmindis.append(min(meandisdist))
            massdmaxdis.append(max(meandisdist))
            
            wmasstmeandis.append(np.mean(wmeantimedis))
            wmasstmindis.append(min(wmeantimedis))
            wmasstmaxdis.append(max(wmeantimedis))
            wmassdmeandis.append(np.mean(wmeandisdist))
            wmassdmindis.append(min(wmeandisdist))
            wmassdmaxdis.append(max(wmeandisdist))
    if Model[0] == 'ROMS':
        
        tmeandis=(np.mean(romstmeandis))
        tmindis=(min(romstmindis))
        tmaxdis=(max(romstmaxdis))
        dmeandis=(np.mean(romsdmeandis))
        dmindis=(min(romsdmindis))
        dmaxdis=(max(romsdmaxdis))
        
        wtmeandis=(np.mean(wromstmeandis))
        wtmindis=(min(wromstmindis))
        wtmaxdis=(max(wromstmaxdis))
        wdmeandis=(np.mean(wromsdmeandis))
        wdmindis=(min(wromsdmindis))
        wdmaxdis=(max(wromsdmaxdis))
    if Model[0] == '30yr':
        tmeandis=(np.mean(yrtmeandis))
        tmindis=(min(yrtmindis))
        tmaxdis=(max(yrtmaxdis))
        dmeandis=(np.mean(yrdmeandis))
        dmindis=(min(yrdmindis))
        dmaxdis=(max(yrdmaxdis))
        
        wtmeandis=(np.mean(wyrtmeandis))
        wtmindis=(min(wyrtmindis))
        wtmaxdis=(max(wyrtmaxdis))
        wdmeandis=(np.mean(wyrdmeandis))
        wdmindis=(min(wyrdmindis))
        wdmaxdis=(max(wyrdmaxdis))        
    if Model[0] == 'GOM3':
        tmeandis=(np.mean(gomtmeandis))
        tmindis=(min(gomtmindis))
        tmaxdis=(max(gomtmaxdis))
        dmeandis=(np.mean(gomdmeandis))
        dmindis=(min(gomdmindis))
        dmaxdis=(max(gomdmaxdis))
        
        wtmeandis=(np.mean(wgomtmeandis))
        wtmindis=(min(wgomtmindis))
        wtmaxdis=(max(wgomtmaxdis))
        wdmeandis=(np.mean(wgomdmeandis))
        wdmindis=(min(wgomdmindis))
        wdmaxdis=(max(wgomdmaxdis))
    if Model[0] == 'massbay':
        tmeandis=(np.mean(masstmeandis))
        tmindis=(min(masstmindis))
        tmaxdis=(max(masstmaxdis))
        dmeandis=(np.mean(massdmeandis))
        dmindis=(min(massdmindis))
        dmaxdis=(max(massdmaxdis))
        
        wtmeandis=(np.mean(wmasstmeandis))
        wtmindis=(min(wmasstmindis))
        wtmaxdis=(max(wmasstmaxdis))
        wdmeandis=(np.mean(wmassdmeandis))
        wdmindis=(min(wmassdmindis))
        wdmaxdis=(max(wmassdmaxdis))
    data=[]
    wdata=[]
    data.append(tmeandis)
    data.append(tmindis)
    data.append(tmaxdis)
    data.append(dmeandis)
    data.append(dmindis)
    data.append(dmaxdis)
    
    wdata.append(wtmeandis)
    wdata.append(wtmindis)
    wdata.append(wtmaxdis)
    wdata.append(wdmeandis)
    wdata.append(wdmindis)
    wdata.append(wdmaxdis)
    print 'data',data
    print 'wdata',wdata
    hhhhhhhhh.append(data)
    hhhhhhhhh.append(data)
    #fh=['ids']
    #writer.writerow(fh)
    #writer.writerow(hahhahahah)
    #writer.writerow(a1)
    #writer.writerow(data)
    #writer.writerow(a2)
    #writer.writerow(wdata)
    if(data[4]>wdata[4]):
        t=z
        e=e
        z=(t+e)/2
        a1=(t+z)/2
        a2=(z+e)/2
        print 'a1',a1
        print 'a2',a2
    else:
        t=t
        e=z
        z=(t+e)/2
        a1=(t+z)/2
        a2=(z+e)/2
        print 'a1',a1
        print 'a2',a2
wind=(a1+a2)/2
print 'wind',wind
print 'hhhhhhhh',hhhhhhhhh   