import array as arr
from ctypes.wintypes import SIZE
from datetime import datetime, timedelta
from turtle import st 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, legend, xlabel, ylabel
import matplotlib.dates as mdates
import pandas as pd
from tkinter import messagebox
from func.Seach_file import tim_file,read_txt,vitridat
from scipy import interpolate
def interpolate_dataframe(df):
    df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M')
    # Chuyển cột 'time' thành dạng số giây kể từ thời điểm ban đầu
    df['time_seconds'] = (df['time'] - df['time'].min()).dt.total_seconds()
    start_time = df['time'].min()
    end_time = df['time'].max()
    hourly_timestamps = pd.date_range(start_time, end_time, freq='H')
    data = pd.DataFrame()
    data['time'] = hourly_timestamps
    for col in df.iloc[:,1:].columns:
        # tao ham noi suy
        f = interpolate.interp1d(df['time_seconds'], df[col], kind='linear', fill_value="extrapolate")
        # Chuyển các timestamp thành số giây kể từ thời điểm ban đầu
        hourly_timestamps_seconds = (hourly_timestamps - df['time'].min()).total_seconds()
        # nội suy value
        interpolated_values = f(hourly_timestamps_seconds)
        # tạo DataFrame
        result_df = pd.DataFrame({'time': hourly_timestamps, col: interpolated_values})
        data = data.merge(result_df,how='left',on='time')
    return data
def dothi_tvhn():
    pth = tim_file(read_txt('path_tin/DATA_EXCEL.txt'),'.xlsx')
    now = datetime.now()
    bd = datetime(now.year,now.month,now.day,7)
    kt = bd - timedelta(days=10)
    df = pd.read_excel(pth,sheet_name='H')
    df.rename(columns={'Ngày':'time'},inplace=True)
    df=df[['time','Dong Tam','Mai Hoa','Tan My','Kien Giang','Le Thuy','Dong Hoi']]
    df['time'] =pd.date_range(start=datetime(2023,7,8,7),periods=len(df['time']), freq="H")
    df = df.loc[(df['time'] >= kt) & (df['time'] <= bd) ]
    df_td =df
    # print(df)
    # lay gia tri du bao de ve
    dfdb =  pd.read_excel(pth,sheet_name='TVHN')
    db = dfdb.iloc[1:7,4:8].T

    db['time'] = pd.date_range(start=bd+timedelta(hours=6),periods=4, freq="6H")
    db = db.reset_index(drop=True) # bo index
    db.rename(columns={1:'Mai Hoa',2:'Tan My',3:'Le Thuy',4:'Dong Hoi',5:'Dong Tam',6:'Kien Giang',},inplace=True)
    db = db[['time','Dong Tam','Kien Giang','Le Thuy']]
    
    df = pd.concat([df, db], ignore_index=True)

    # ve song gianh
    fig, ax  = plt.subplots(figsize=(20, 12))
    ax.plot(df_td['time'],df_td['Dong Tam'],color = 'r')
    ax.plot(df_td['time'],df_td['Mai Hoa'],color = 'black')
    ax.plot(df_td['time'],df_td['Tan My'],color = 'b')
    # song Gianh
    df_gianh = pd.read_excel(pth,sheet_name='TVHN')
    df_gianh = df_gianh[['time','Mai Hoa','Tan My','Le Thuy','Dong Hoi','Dong Tam','Kien Giang']]
    
    db = df.tail(5)
    db_ns = interpolate_dataframe(db) # noi suy gia tri
    # print(df_gianh)
    # print(db_ns)
    ax.plot(db_ns['time'],db_ns['Dong Tam'],linestyle = 'dashed',color = 'r')
    ax.plot(db_ns['time'],df_gianh['Mai Hoa'],linestyle = 'dashed',color = 'black')
    ax.plot(db_ns['time'],df_gianh['Tan My'],linestyle = 'dashed',color = 'b')

    # Đặt trục x với khoảng cách là 6 giờ
    six_hour_locator = mdates.HourLocator(interval=6)
    ax.xaxis.set_major_locator(six_hour_locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %Hh'))
    
    # ax.set(title='BIỂU ĐỒ MỰC NƯỚC THỰC ĐO 10 NGÀY',fontsize=30)
    ax.set_xlabel('Thời Gian',size = 15)
    ax.set_ylabel('Mực nước(cm)',size = 15)

    plt.xticks(rotation=60, size=12)
    plt.tight_layout(pad=5)
    plt.title('QUÁ TRÌNH MỰC NƯỚC THỰC ĐO 10 NGÀY VÀ DỰ BÁO 24H TRÊN LƯU VỰC SÔNG GIANH',size = 25)
    plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    plt.legend(['Đồng Tâm thực đo','Mai Hóa thực đo','Tân Mỹ thực đo','Đồng Tâm dự báo','Mai Hóa dự báo','Tân Mỹ dự báo'],prop={'size': 20})
    plt.savefig('image/TVHN_GIANH.jpg')

    # plt.show()
    
    # ve song kien giang
    fig, ax  = plt.subplots(figsize=(20, 12))
    ax.plot(df_td['time'],df_td['Kien Giang'],color = 'r')
    ax.plot(df_td['time'],df_td['Le Thuy'],color = 'black')
    ax.plot(df_td['time'],df_td['Dong Hoi'],color = 'b')
    
    ax.plot(db_ns['time'],db_ns['Kien Giang'],linestyle = 'dashed',color = 'r')
    ax.plot(db_ns['time'],db_ns['Le Thuy'],linestyle = 'dashed',color = 'black')
    ax.plot(db_ns['time'],df_gianh['Dong Hoi'],linestyle = 'dashed',color = 'b')
    
    # Đặt trục x với khoảng cách là 6 giờ
    six_hour_locator = mdates.HourLocator(interval=6)
    ax.xaxis.set_major_locator(six_hour_locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %Hh'))
    
    # ax.set(title='BIỂU ĐỒ MỰC NƯỚC THỰC ĐO 10 NGÀY',fontsize=30)
    ax.set_xlabel('Thời Gian',size = 15)
    ax.set_ylabel('Mực nước(cm)',size = 15)

    plt.xticks(rotation=60, size=12)
    plt.tight_layout(pad=5)
    plt.title('QUÁ TRÌNH MỰC NƯỚC THỰC ĐO 10 NGÀY VÀ DỰ BÁO 24H TRÊN LƯU VỰC SÔNG KIẾN GIANG',size = 25)
    plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    plt.legend(['Kiến Giang thực đo','Lệ Thủy thực đo','Đồng Hới thực đo','Kiến Giang dự báo','Lệ Thủy dự báo','Đồng Hới dự báo'],prop={'size': 20})
    plt.savefig('image/TVHN_KIENGIANG.jpg')
    messagebox.showinfo('Thông báo','OK')
    # plt.show()

def vedothituan():
    pth = tim_file(read_txt('path_tin/DATA_EXCEL.txt'),'.xlsm')
    now = datetime.now()
    bddb = datetime(now.year,now.month,now.day,23)
    now = now - timedelta(days=1)
    bd = datetime(now.year,now.month,now.day,23)
    kt = bd - timedelta(days=60)

    df = pd.read_excel(pth,sheet_name='H')
    df.rename(columns={'Ngày':'time','Trà Khúc':'trakhuc','Sông Vệ':'songve','Trà Bồng\n(Châu Ổ)':'chauo','Trà Câu':'tracau'},inplace=True)
    df=df[['time','chauo','trakhuc','songve','tracau']]
    dt_rang = pd.date_range(start=datetime(2022,1,1,1),periods=len(df['time']), freq="H")
    df['time'] =dt_rang
    df = df.loc[(df['time'] >= kt) & (df['time'] <= bd)]
    data = df.rolling(24*5,min_periods=1).agg(['mean','max','min'])
    data['time']=df['time']
    data = data[(data['time'].dt.hour==23) & ((data['time'].dt.day==1)|(data['time'].dt.day==6)|(data['time'].dt.day==11)|(data['time'].dt.day==16)|(data['time'].dt.day==21)|(data['time'].dt.day==26))]
    data = data.iloc[1:,:]

    # them gia tri du bao vao dataframe
    df = pd.read_excel(pth,sheet_name='TVHV')
    df = df.iloc[2:,5:]
    db = []
    for i in range(4):
        for a in df.iloc[i]:
            db.append(a)
    db.append(bddb)
    data.loc[len(data['time'])] = db
    # print(databd)
    fig, ax  = plt.subplots(2,2,figsize=(20, 12))
    hh = len(data['time'])-1

    ax[0,0].plot(data['time'].head(hh),data['chauo']['mean'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].plot(data['time'].head(hh),data['chauo']['max'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].plot(data['time'].head(hh),data['chauo']['min'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].set_xlabel('Thời Gian',size = 11)
    ax[0,0].set_ylabel('Mực nước(cm)',size = 11)
    ax[0,0].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG TRÀ BỒNG TẠI TRẠM CHÂU Ổ',size=11)
    ax[0,0].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[0,0].grid(color = 'k', linestyle = '--', linewidth = 0.5)

    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['mean'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['max'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['min'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].set_xlabel('Thời Gian',size = 11)
    ax[0,1].set_ylabel('Mực nước(cm)',size = 11)
    ax[0,1].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG TRÀ KHÚC TẠI TRẠM TRÀ KHÚC',size=11)
    ax[0,1].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[0,1].grid(color = 'k', linestyle = '--', linewidth = 0.5)


    ax[1,0].plot(data['time'].head(hh),data['songve']['mean'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].plot(data['time'].head(hh),data['songve']['max'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].plot(data['time'].head(hh),data['songve']['min'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].set_xlabel('Thời Gian',size = 11)
    ax[1,0].set_ylabel('Mực nước(cm)',size = 11)
    ax[1,0].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG VỆ TẠI TRẠM SÔNG VỆ',size=11)
    ax[1,0].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[1,0].grid(color = 'k', linestyle = '--', linewidth = 0.5)


    ax[1,1].plot(data['time'].head(hh),data['tracau']['mean'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].plot(data['time'].head(hh),data['tracau']['max'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].plot(data['time'].head(hh),data['tracau']['min'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].set_xlabel('Thời Gian',size = 11)
    ax[1,1].set_ylabel('Mực nước(cm)',size = 11)
    ax[1,1].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG TRÀ CÂU TẠI TRẠM TRÀ CÂU',size=11)
    ax[1,1].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[1,1].grid(color = 'k', linestyle = '--', linewidth = 0.5)

    plt.tight_layout(pad=4)
    plt.savefig('image/Dothituan.png')
    # plt.show()
    messagebox.showinfo('Thông báo','OK!')

# vedothituan()

def vedothithang():
    pth = tim_file(read_txt('path_tin/DATA_EXCEL.txt'),'.xlsm')
    now = datetime.now()
    tgt = datetime.now()
    bddb = datetime(now.year,now.month,now.day,1)
    now = now - timedelta(days=1)
    bd = datetime(now.year,now.month,now.day,23)
    kt = datetime(2022,1,1,1)

    df = pd.read_excel(pth,sheet_name='H')
    df.rename(columns={'Ngày':'time','Trà Khúc':'trakhuc','Sông Vệ':'songve','Trà Bồng\n(Châu Ổ)':'chauo','Trà Câu':'tracau'},inplace=True)
    df=df[['time','chauo','trakhuc','songve','tracau']]
    dt_rang = pd.date_range(start=datetime(2022,1,1,1),periods=len(df['time']), freq="H")
    df['time'] =dt_rang
    df = df.loc[(df['time'] >= kt) & (df['time'] <= bd)]
    # print(df)
    
    
    data = df.rolling(24*30,min_periods=1).agg(['mean','max','min'])
    print(data)
    data['time']=df['time']
    data = data[(data['time'].dt.hour==1) & (data['time'].dt.day==1)]
    print(data)
    data = data.iloc[1:,:]
    print(data)
    # them gia tri du bao vao dataframe
    df = pd.read_excel(pth,sheet_name='TVHD')
    df = df.iloc[2:,-3:]
    # print(df)
    db = []
    for i in range(4):
        for a in df.iloc[i]:
            db.append(a)
    db.append(bddb)
    
    data.loc[len(data['time'])] = db
    print(data)
    fig, ax  = plt.subplots(2,2,figsize=(20, 12))
    hh = len(data['time'])-1

    ax[0,0].plot(data['time'].head(hh),data['chauo']['mean'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].plot(data['time'].head(hh),data['chauo']['max'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].plot(data['time'].head(hh),data['chauo']['min'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].set_xlabel('Thời Gian',size = 11)
    ax[0,0].set_ylabel('Mực nước(cm)',size = 11)
    img_name = 'ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO THÁNG {} SÔNG TRÀ BỒNG TẠI TRẠM CHÂU Ổ'.format(tgt.strftime('%m'))
    ax[0,0].set_title(img_name,size=11)
    ax[0,0].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[0,0].grid(color = 'k', linestyle = '--', linewidth = 0.5)

    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['mean'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['max'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['min'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].set_xlabel('Thời Gian',size = 11)
    ax[0,1].set_ylabel('Mực nước(cm)',size = 11)
    ax[0,1].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO THÁNG {} SÔNG TRÀ KHÚC TẠI TRẠM TRÀ KHÚC'.format(tgt.strftime('%m')),size=11)
    ax[0,1].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[0,1].grid(color = 'k', linestyle = '--', linewidth = 0.5)


    ax[1,0].plot(data['time'].head(hh),data['songve']['mean'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].plot(data['time'].head(hh),data['songve']['max'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].plot(data['time'].head(hh),data['songve']['min'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].set_xlabel('Thời Gian',size = 11)
    ax[1,0].set_ylabel('Mực nước(cm)',size = 11)
    ax[1,0].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO THÁNG {} SÔNG VỆ TẠI TRẠM SÔNG VỆ'.format(tgt.strftime('%m')),size=11)
    ax[1,0].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[1,0].grid(color = 'k', linestyle = '--', linewidth = 0.5)


    ax[1,1].plot(data['time'].head(hh),data['tracau']['mean'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].plot(data['time'].head(hh),data['tracau']['max'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].plot(data['time'].head(hh),data['tracau']['min'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].set_xlabel('Thời Gian',size = 11)
    ax[1,1].set_ylabel('Mực nước(cm)',size = 11)
    ax[1,1].set_title(('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO THÁNG {} SÔNG TRÀ CÂU TẠI TRẠM TRÀ CÂU').format(tgt.strftime('%m')),size=11)
    ax[1,1].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[1,1].grid(color = 'k', linestyle = '--', linewidth = 0.5)

    plt.tight_layout(pad=4)
    plt.savefig('image/Dothithang.png')
    messagebox.showinfo('Thông báo','OK!')
    
# plt.show()
# vedothithang()

def vedothituan10():
    pth = tim_file(read_txt('path_tin/DATA_EXCEL.txt'),'.xlsm')
    now = datetime.now()
    bddb = datetime(now.year,now.month,now.day,23)
    now = now - timedelta(days=1)
    bd = datetime(now.year,now.month,now.day,23)
    kt = bd - timedelta(days=90)

    df = pd.read_excel(pth,sheet_name='H')
    df.rename(columns={'Ngày':'time','Trà Khúc':'trakhuc','Sông Vệ':'songve','Trà Bồng\n(Châu Ổ)':'chauo','Trà Câu':'tracau'},inplace=True)
    df=df[['time','chauo','trakhuc','songve','tracau']]
    dt_rang = pd.date_range(start=datetime(2022,1,1,1),periods=len(df['time']), freq="H")
    df['time'] =dt_rang
    df = df.loc[(df['time'] >= kt) & (df['time'] <= (bd + timedelta(days=1)))]
    data = df.rolling(24*10,min_periods=1).agg(['mean','max','min'])
    data['time']=df['time']
    data = data[(data['time'].dt.hour==23) & ((data['time'].dt.day==1)|(data['time'].dt.day==11)|(data['time'].dt.day==21))]
    data = data.iloc[1:,:]
    # print(data)
    # them gia tri du bao vao dataframe
    df = pd.read_excel(pth,sheet_name='TVHV10')
    df = df.iloc[2:,11:14]
    # print(df)
    db = []
    for i in range(4):
        for a in df.iloc[i]:
            db.append(a)
    
    db.append(bddb+timedelta(days=10))
    # print(db)
    data.loc[len(data['time'])] = db
    # print(data)
    fig, ax  = plt.subplots(2,2,figsize=(20, 12))
    hh = len(data['time'])-1

    ax[0,0].plot(data['time'].head(hh),data['chauo']['mean'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].plot(data['time'].head(hh),data['chauo']['max'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].plot(data['time'].head(hh),data['chauo']['min'].head(hh))
    ax[0,0].plot(data['time'].tail(2),data['chauo']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,0].set_xlabel('Thời Gian',size = 11)
    ax[0,0].set_ylabel('Mực nước(cm)',size = 11)
    ax[0,0].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG TRÀ BỒNG TẠI TRẠM CHÂU Ổ',size=11)
    ax[0,0].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[0,0].grid(color = 'k', linestyle = '--', linewidth = 0.5)

    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['mean'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['max'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].plot(data['time'].head(hh),data['trakhuc']['min'].head(hh))
    ax[0,1].plot(data['time'].tail(2),data['trakhuc']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[0,1].set_xlabel('Thời Gian',size = 11)
    ax[0,1].set_ylabel('Mực nước(cm)',size = 11)
    ax[0,1].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG TRÀ KHÚC TẠI TRẠM TRÀ KHÚC',size=11)
    ax[0,1].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[0,1].grid(color = 'k', linestyle = '--', linewidth = 0.5)


    ax[1,0].plot(data['time'].head(hh),data['songve']['mean'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].plot(data['time'].head(hh),data['songve']['max'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].plot(data['time'].head(hh),data['songve']['min'].head(hh))
    ax[1,0].plot(data['time'].tail(2),data['songve']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,0].set_xlabel('Thời Gian',size = 11)
    ax[1,0].set_ylabel('Mực nước(cm)',size = 11)
    ax[1,0].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG VỆ TẠI TRẠM SÔNG VỆ',size=11)
    ax[1,0].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[1,0].grid(color = 'k', linestyle = '--', linewidth = 0.5)


    ax[1,1].plot(data['time'].head(hh),data['tracau']['mean'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['mean'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].plot(data['time'].head(hh),data['tracau']['max'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['max'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].plot(data['time'].head(hh),data['tracau']['min'].head(hh))
    ax[1,1].plot(data['time'].tail(2),data['tracau']['min'].tail(2),linestyle = 'dashed',marker = 'o')
    ax[1,1].set_xlabel('Thời Gian',size = 11)
    ax[1,1].set_ylabel('Mực nước(cm)',size = 11)
    ax[1,1].set_title('ĐƯỜNG QUÁ TRÌNH MỰC NƯỚC THỰC ĐO VÀ DỰ BÁO TUẦN SÔNG TRÀ CÂU TẠI TRẠM TRÀ CÂU',size=11)
    ax[1,1].legend(['Trung bình','Trung bình dự báo','Max','Max dự báo','Min','Min dự báo'],prop={'size': 11})
    ax[1,1].grid(color = 'k', linestyle = '--', linewidth = 0.5)

    plt.tight_layout(pad=4)
    plt.savefig('image/Dothituan10.png')
    messagebox.showinfo('Thông báo','OK!')
# vedothituan10()