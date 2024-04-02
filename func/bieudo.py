import pandas as pd
import numpy as np
from datetime import datetime,timedelta
# from func.Seach_file import tim_file,read_txt,vitridat
from tkinter import messagebox
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, legend, xlabel, ylabel
import matplotlib.dates as mdates
# from CDH_TTB_API import TTB_API_songtranh2
from scipy import interpolate
import seaborn as sns


def interpolate_dataframe(df):
    df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M')
    # Chuyển cột 'time' thành dạng số giây kể từ thời điểm ban đầu
    df['time_seconds'] = (df['time'] - df['time'].min()).dt.total_seconds()
    start_time = df['time'].min()
    end_time = df['time'].max()
    hourly_timestamps = pd.date_range(start_time, end_time, freq='H')
    data = pd.DataFrame()
    data['time'] = hourly_timestamps
    print(data)
    for col in df.iloc[:,1:].columns:
        # tao ham noi suy
        f = interpolate.interp1d(df['time_seconds'], df[col], kind='linear', fill_value="extrapolate")
        print(f)
        # Chuyển các timestamp thành số giây kể từ thời điểm ban đầu
        hourly_timestamps_seconds = (hourly_timestamps - df['time'].min()).total_seconds()
        print(hourly_timestamps_seconds)
        # nội suy value
        interpolated_values = f(hourly_timestamps_seconds)
        print(interpolated_values)
        # tạo DataFrame
        result_df = pd.DataFrame({'time': hourly_timestamps, col: interpolated_values})
        data = data.merge(result_df,how='left',on='time')
    return data
        
def ve_H_hochua():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,7)
    bd = kt - timedelta(days=30)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='H')
    # tram = pd.read_csv('TS_ID/TTB/songtranh2.txt')
    tram = pd.read_csv(r'D:\PM_PYTHON\SONGTRANH_WEB\TS_ID\TTB\songtranh2.txt')
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
    data = data.replace(0,np.nan)
    data= data.interpolate(method='linear')
    data.reset_index(drop=False,inplace=True)
    # data = interpolate_dataframe(data)
    # print(data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['time'], data['mucnuoc'], color='r', label='Hdr')
    # ax.plot(data['time'], data['Hnt'], color='black', label='Hnt')
    ax.set_xlabel('Thời gian',size = 20)
    ax.set_ylabel('Mực nước',size = 20)
    ax.set_title('Mực nước hồ chứa',size = 20)
    ax.legend(['Sông Tranh 2'])
    plt.xticks(rotation=60, size=12)
    plt.xticks(rotation=60, size=12)
    plt.tight_layout(pad=5)
    plt.title('QUÁ TRÌNH MỰC NƯỚC THỰC ĐO 10 NGÀY',size = 25)
    plt.legend(['Đakdrinh','Nước Trong'],prop={'size': 20})
    plt.show()
    return fig
    # return hdr,hnt,hnn,w_dr,w_nt
    
# ve_H_hochua()   
    
def ve_Q_veho():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,now.hour)
    bd = kt - timedelta(days=30)
    dfname = pd.read_csv('TS_ID/CDH/CDH_hochua.txt',sep="\s+",header=None)
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
    data = data.replace(0,np.nan)
    data= data.interpolate(method='linear')
    data.reset_index(drop=False,inplace=True)
    # data = interpolate_dataframe(data)
    # print(data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['time'], data['Qvedr'], color='r', label='Q')
    # ax.plot(data['time'], data['Qrakhoihodr'], color='black', label='Qra')
    ax.set_xlabel('Thời gian',size = 20)
    ax.set_ylabel('Lưu Lượng',size = 20)
    ax.set_title('Lưu lượng',size = 20)
    ax.legend(['Lưu lượng về'])
    plt.xticks(rotation=60, size=12)
    # plt.xticks(rotation=60, size=12)
    # plt.tight_layout(pad=5)
    # plt.title('QUÁ TRÌNH MỰC NƯỚC THỰC ĐO 10 NGÀY',size = 25)
    # plt.legend(['Đakdrinh','Nước Trong'],prop={'size': 20})
    # plt.show()
    return fig

def Bieudo_Q_H(bd,kt):
    # now = datetime.now()
    # kt = datetime(now.year,now.month,now.day,7)
    # bd = kt - timedelta(days=10)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='h')
    tram = pd.read_csv('TS_ID/TTB/songtranh2.txt')
    # tram = pd.read_csv(r'D:\PM_PYTHON\SONGTRANH_WEB\TS_ID\TTB\songtranh2.txt')
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
    data = data.replace(0,np.nan)
    # data= data.interpolate(method='linear')
    # data = data.applymap("{0:.2f}".format)
    data.reset_index(drop=False,inplace=True)
    # vcl = data[data['mucnuoc'] > 178]
    # print(vcl)
    # print(df_lu)
    # ve muc nuoc
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data['time'], data['mucnuoc'], color='black', label='Thực đo')
    # ax.plot(df_db_h['time'], df_db_h['Hdb'], color='r',linestyle = 'dashed', label='Dự báo')
    # ax.plot(data['time'], data['Qrakhoihodr'], color='black', label='Qra')
    ax.set_xlabel('Thời gian',size = 5)
    ax.set_ylabel('Mực nước (m)',size = 5)
    ax.set_title('Đường quá trình mực nước Hồ Sông Tranh 2',size = 10)
    ax.legend(['Thực đo'])
    ax.grid(True,linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
    ax.set_facecolor((1.0, 1.00, 0.196, 0.5)) 
    plt.xticks(rotation=90, size=5)
    plt.yticks(rotation=0, size=5)
    plt.tight_layout(pad=1)
    
    # ve Q ve ho
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    # Điều chỉnh lề trên, dưới, trái và phải
    top_margin = 0.1  # Thay đổi lề trên (top margin)
    bottom_margin = 0.05  # Thay đổi lề dưới (bottom margin)
    left_margin = 0.05  # Thay đổi lề trái (left margin)
    right_margin = 0.1  # Thay đổi lề phải (right margin)
    ax1.figure.subplots_adjust(top=top_margin, bottom=bottom_margin, left=left_margin, right=right_margin)
    
    ax1.plot(data['time'], data['qden'], color='black', label='Q về hồ')
    ax1.plot(data['time'], data['qxa'], color='r', label='Q điều tiết')
    ax1.set_xlabel('Thời gian',size = 5)
    ax1.set_ylabel('Lưu lượng (m3/s)',size = 5)
    ax1.set_title('Đường quá trình lưu lượng về hồ Sông Tranh 2',size = 10)
    ax1.legend(['Q về hồ','Q điều tiết'])
    ax1.grid(True,linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
    ax1.set_facecolor((1.0, 1.00, 0.196, 0.5)) 
    plt.xticks(rotation=90, size=5)
    plt.yticks(rotation=0, size=5)
    plt.tight_layout(pad=1)
    # plt.title('QUÁ TRÌNH MỰC NƯỚC THỰC ĐO 10 NGÀY',size = 25)
    # plt.legend(['Đakdrinh','Nước Trong'],prop={'size': 20})
    # plt.show()
    # print(df_lu['H'].iloc[-1])
    

    
    df_mua = data.drop(['mucnuoc','qden','qxa'],axis=1)
    # print(df_mua)
    # ghichu = []
    # for a in df_mua.columns[1:]:
    #     ax2.bar(df_mua['time'], df_mua[a])
    #     ghichu.append(a)
    # # ax1.plot(data['time'], data['qden'], color='black', label='Q về hồ')
    # # ax1.plot(data['time'], data['qxa'], color='r', label='Q điều tiết')
    # ax2.set_xlabel('Thời gian',size = 5)
    # ax2.set_ylabel('Lượng mưa (mm)',size = 5)
    # ax2.set_title('Biểu đồ mưa lưu vực hồ Sông Tranh 2',size = 10)
    # # ax2.legend(ghichu)
    # ax2.grid(True,linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
    # ax2.set_facecolor((1.0, 1.00, 0.196, 0.5)) 
    # plt.xticks(rotation=90, size=5)
    # plt.yticks(rotation=0, size=5)
    # plt.tight_layout(pad=1)
 
    data['mucnuoc'] =  data['mucnuoc'].map('{0:.2f}'.format)
    data['qden'] =  data['qden'].map('{0:.1f}'.format)
    data['qxa'] =  data['qxa'].map('{0:.1f}'.format)
    data.rename(columns={'time':'Thời gian','mucnuoc':'Mực nước (m)','qden':'Q đến (m3/s)','qxa':'Q điều tiết (m3/s)'},inplace=True)
    # name_eng = ['TRABUI', 'tracang', 'tradon', 'tragiac', 'traleng', 'tralinh','TRAMAI', 'UBNDHnamTM', 'tramdapst2', 'tranam2', 'travan']
    name_viet = ['time','Trà Bùi', 'Trà Căng', 'Trà Dơn', 'Trà Giác', 'Trà Leng', 'Trà Linh','Trà Mai', 'UBNDHnamTM', 'Trà Đốc(Đập chính)', 'Trà Nam', 'Trà Vân']
    df_mua.columns =name_viet
    return fig,fig1,df_mua,data



def Mucnuoc_songtranh():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,now.hour)
    bd = kt - timedelta(days=1)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='h')
    tram = pd.read_csv('TS_ID/TTB/songtranh2.txt')
    # tram = pd.read_csv(r'D:\PM_PYTHON\SONGTRANH_WEB\TS_ID\TTB\songtranh2.txt')
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
    data = data.replace(0,np.nan)
    data= data.interpolate(method='linear')
    data.reset_index(drop=False,inplace=True)
    return data['mucnuoc'].iloc[-1]

def vebieudomua(df_mua):
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    # Điều chỉnh lề trên, dưới, trái và phải
    top_margin = 0.1  # Thay đổi lề trên (top margin)
    bottom_margin = 0.05  # Thay đổi lề dưới (bottom margin)
    left_margin = 0.05  # Thay đổi lề trái (left margin)
    right_margin = 0.1  # Thay đổi lề phải (right margin)
    ax2.figure.subplots_adjust(top=top_margin, bottom=bottom_margin, left=left_margin, right=right_margin)
    # ax2.bar(data['time'], data['tramdapst2'], color='skyblue')
    ghichu =[]
    for a in df_mua.columns[1:]:
        ax2.bar(df_mua['time'], df_mua[a])
        ghichu.append(a)
    ax2.set_xlabel('Thời gian',size = 5)
    ax2.set_ylabel('Lượng mưa (mm)',size = 5)
    ax2.set_title('Biểu đồ trạm {}'.format(ghichu[0]),size = 10)
    ax2.legend(ghichu)
    ax2.grid(True,linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
    ax2.set_facecolor((1.0, 1.00, 0.196, 0.5)) 
    plt.xticks(rotation=90, size=5)
    plt.yticks(rotation=0, size=5)
    plt.tight_layout(pad=1)
    plt.show()
    return fig2
    


# Bieudo_Q_H()