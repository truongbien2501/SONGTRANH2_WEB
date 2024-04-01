import pandas as pd
import numpy as np
from datetime import datetime,timedelta
# from func.Seach_file import tim_file,read_txt,vitridat
from tkinter import messagebox
from openpyxl import load_workbook
from win32com import client
import time
def TTB_API_songtranh2():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,7)
    bd = kt - timedelta(days=30)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='H')
    tram = pd.read_csv('TS_ID/TTB/songtranh2.txt')
    for item in zip(tram.Matram,tram.tentram,tram.TAB):
    # print(item[0],item[2],item[1])
        pth = 'http://113.160.225.84:2018/API_TTB/XEM/solieu.php?matram={}&ten_table={}&sophut=60&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(item[0],item[2],bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        df = pd.read_html(pth)
        df[0].rename(columns={"thoi gian":'time','so lieu':item[1]},inplace=True)
        df = df[0].drop('Ma tram',axis=1)
        df['time'] = pd.to_datetime(df['time'])
        data = data.merge(df,how='left',on='time')
    data.set_index('time',inplace=True)
    data = data[data.index.minute == 0]
    data =data.astype(float)
    return data


def TTB_API_mucnuoc():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,7)
    bd = kt - timedelta(days=1)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='T')
    tram = pd.read_csv('TS_ID/TTB/TTB_H_ODA.txt')
    for item in zip(tram.Matram,tram.tentram,tram.TAB):
    # print(item[0],item[2],item[1])
        pth = 'http://113.160.225.84:2018/API_TTB/XEM/solieu.php?matram={}&ten_table={}&sophut=1&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(item[0],item[2],bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        df = pd.read_html(pth)
        df[0].rename(columns={"thoi gian":'time','so lieu':item[1]},inplace=True)
        df = df[0].drop('Ma tram',axis=1)
        df['time'] = pd.to_datetime(df['time'])
        data = data.merge(df,how='left',on='time')
    data.set_index('time',inplace=True)
    data = data[data.index.minute == 0]

    data = data[['Son Giang','Tra Khuc','An Chi','Song Ve','Chau O','Tra Cau','Binh Dong','Dung Quat Idro']]*100
    data =data.astype(float)
    return data
def CDH_API_mucnuoc():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,7)
    bd = kt - timedelta(days=1)
    dfname = pd.read_csv('TS_ID/CDH/CDH_H_QNGA.txt',sep="\s+",header=None)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='H')
    
    for tsid in zip(dfname[0],dfname[1]):
        url = 'https://cdh.vnmha.gov.vn/KiWIS/KiWIS?http://slportal.kttv.gov.vn/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={}&from={}&to={}'
        df = pd.read_html(url.format(tsid[0],bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d')))
        for i in df:
            i = i.iloc[4:,:].dropna()
            i.rename(columns={0:'time',1:tsid[1]},inplace=True)
            i['time'] = pd.to_datetime(i['time'])
            i['time'] = i['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            i['time'] = pd.to_datetime(i['time'])
            data = data.merge(i,how='left',on='time')
    data.set_index('time',inplace=True)
    data =data.astype(float)
    data['sg_oda'].update(data['sg_tc'])
    data['ac_oda'].update(data['ac_tc'])
    return data

def CDH_API_muaoda():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,7)
    bd = kt - timedelta(hours=25)
    dfname = pd.read_csv('TS_ID/CDH/CDH_MUA_ODA.txt',sep="\s+",header=None)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='H')
    for tsid in zip(dfname[0],dfname[1]):
        url = 'https://cdh.vnmha.gov.vn/KiWIS/KiWIS?http://slportal.kttv.gov.vn/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={}&from={}&to={}'
        df = pd.read_html(url.format(tsid[0],bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d')))
        for i in df:
            i = i.iloc[4:,:].dropna()
            i.rename(columns={0:'time',1:tsid[1]},inplace=True)
            i['time'] = pd.to_datetime(i['time'])
            i['time'] = i['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            i['time'] = pd.to_datetime(i['time'])
            data = data.merge(i,how='left',on='time')
    data.set_index('time',inplace=True)
    data =data.astype(float)
    data.fillna(method='ffill', inplace=True) # thay the nhung gia tri trong bang nan
    data = data.diff()
    tgg = bd + timedelta(hours=1)
    data = data.loc[data.index >= tgg]
    return data
   
def CDH_API_muavrain():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,7)
    bd = kt - timedelta(hours=25)
    dfname = pd.read_csv('TS_ID/CDH/CDH_MUA_VRAIN.txt',sep="\s+",header=None)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='T')
    for tsid in zip(dfname[0],dfname[1]):
        url = 'https://cdh.vnmha.gov.vn/KiWIS/KiWIS?http://slportal.kttv.gov.vn/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={}&from={}&to={}'
        df = pd.read_html(url.format(tsid[0],bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d')))
        for i in df:
            i = i.iloc[4:,:].dropna()
            i.rename(columns={0:'time',1:tsid[1]},inplace=True)
            i['time'] = pd.to_datetime(i['time'])
            i['time'] = i['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            i['time'] = pd.to_datetime(i['time'])
            data = data.merge(i,how='left',on='time')
    data.set_index('time',inplace=True)
    muagio = data.rolling(60,min_periods=1).sum()
    muagio = muagio[muagio.index.minute == 0]
    muagio =muagio.astype(float)
    tgg = bd + timedelta(hours=1)
    muagio = muagio.loc[muagio.index >= tgg]
    return muagio
        
def H_hochua():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,now.hour)
    bd = kt - timedelta(days=30)
    dfname = pd.read_csv('TS_ID/CDH/CDH_H_hochua.txt',sep="\s+",header=None)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='H')
    for tsid in zip(dfname[0],dfname[1]):
        url = 'https://cdh.vnmha.gov.vn/KiWIS/KiWIS?http://slportal.kttv.gov.vn/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={}&from={}&to={}'
        df = pd.read_html(url.format(tsid[0],bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d')))
        for i in df:
            i = i.iloc[4:,:].dropna()
            i.rename(columns={0:'time',1:tsid[1]},inplace=True)
            i['time'] = pd.to_datetime(i['time'])
            i['time'] = i['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            i['time'] = pd.to_datetime(i['time'])
            data = data.merge(i,how='left',on='time')
    data.set_index('time',inplace=True)
    data =data.astype(float)
    df_dr = data[['Hdr']]
    df_dr = df_dr[df_dr['Hdr']>0]
    hdr =df_dr['Hdr'].iloc[-1]
    
    df_nt = data[['Hnt']]
    df_tn = df_nt[df_nt['Hnt']>0]
    hnt = df_tn['Hnt'].iloc[-1]
    
    # df_nn = data[['Hnn']]
    # df_nn = df_nn[df_nn['Hnn']>0]
    # hnn= df_nn['Hnn'].iloc[-1]
    
    dungtich = pd.read_excel('data/hochua.xlsx',sheet_name='hochua')
    dt_dr = dungtich[['hdr','wdr']]
    dt_dr['hdr'] = dt_dr['hdr'].map('{0:.2f}'.format)
    dt_dr = dt_dr.loc[dt_dr['hdr']=='{:.2f}'.format(hdr)]
    w_dr = dt_dr['wdr'].values[0]/248.51*100
    
    dt_nt = dungtich[['hnt','wnt']].dropna()
    dt_nt['hnt'] = dt_nt['hnt'].map('{0:.1f}'.format)
    dt_nt = dt_nt.loc[dt_nt['hnt']=='{:.1f}'.format(hnt)]
    w_nt = dt_nt['wnt'].values[0]/289.5*100

    return hdr,hnt,129,w_dr,w_nt
    # return hdr,hnt,hnn,w_dr,w_nt

def dungtich_hochua(h_dr,h_nt):
    dungtich = pd.read_excel('data/hochua.xlsx',sheet_name='hochua')
    dt_dr = dungtich[['hdr','wdr']]
    dt_dr['hdr'] = dt_dr['hdr'].map('{0:.2f}'.format)
    dt_dr = dt_dr.loc[dt_dr['hdr']=='{:.2f}'.format(h_dr)]
    w_dr = dt_dr['wdr'].values[0]/248.51*100

    dt_nt = dungtich[['hnt','wnt']].dropna()
    dt_nt['hnt'] = dt_nt['hnt'].map('{0:.1f}'.format)
    dt_nt = dt_nt.loc[dt_nt['hnt']=='{:.1f}'.format(h_nt)]
    w_nt = dt_nt['wnt'].values[0]/289.5*100
    return w_dr,w_nt

def H_excel():
    now = datetime.now()
    # df = pd.read_excel('data/DR_THUYVAN.xlsx',sheet_name='DRHN')
    df = pd.read_excel(r'D:\PM_PYTHON\APP_WEB\data\DR_THUYVAN.xlsx',sheet_name='DRHN')
    kt = now - timedelta(hours=24)
    df = df.iloc[1:,:21]
    df['time'] = pd.date_range(start=datetime(now.year,8,31,13), periods=len(df['time']), freq="6H")
    df["Hdb"] = df["Hdb"].apply(lambda x: f"{x}")
    # print(df[df['Hdb'].isnull() ==False])
    
    df_lu = pd.read_excel(r'D:\PM_PYTHON\APP_WEB\data\DR_THUYVAN.xlsx',sheet_name='LULU')
    df_lu = df_lu.iloc[3:,:21]
    df_lu['time'] = pd.date_range(start=datetime(now.year,9,1), periods=len(df_lu['time']), freq="H")
    df_lu['H'].update(df['Htd'])
    print(df_lu['H'])
    df_lu = df_lu[['time','H']]
    df = df[['time','Htd','Hdb','qtd','qdb']]
    return df,df_lu
# H_excel()