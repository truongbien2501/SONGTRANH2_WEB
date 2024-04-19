import io
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import paramiko
import pyautogui as pa
import pandas as pd
from ftplib import FTP
from PIL import Image
# Hàm để ánh xạ và đổi hướng
def convert_direction(x):
    if x >= 0:
        return x  # Giữ nguyên giá trị dương
    else:
        return x + 360  # Cộng 360 để chuyển sang giá trị dương

def map_wind_direction(x):
    return (
        'N' if 348.75 <= x <= 11.25 else
        'NNE' if 11.25 < x <= 33.75 else
        'NE' if 33.75 < x <= 56.25 else
        'ENE' if 56.25 < x <= 78.75 else
        'E' if 78.75 < x <= 101.25 else
        'ESE' if 101.25 < x <= 123.75 else
        'SE' if 123.75 < x <= 146.25 else
        'SSE' if 146.25 < x <= 168.75 else
        'S' if 168.75 < x <= 191.25 else
        'SSW' if 191.25 < x <= 213.75 else
        'SW' if 213.75 < x <= 236.25 else
        'WSW' if 236.25 < x <= 258.75 else
        'W' if 258.75 < x <= 281.25 else
        'WNW' if 281.25 < x <= 303.75 else
        'NW' if 303.75 < x <= 326.25 else
        'NNW'
    )


def check_file_exists(ftp, file_path):
    file_list = ftp.nlst()  # Lấy danh sách các file và thư mục trên máy chủ
    return file_path in file_list

def read_ecmwf_st(ngay,tram,tg_db):
    # Thay đổi thông tin theo máy chủ FTP của bạn
    ftp_host = '222.255.11.68'
    ftp_user = 'cnttuser'
    ftp_password = 'cnTT123'
    found_file = False
    for x in range(0,5):
        if found_file:  # Nếu đã tìm thấy file, thoát khỏi vòng lặp
            break
        now = datetime.now()
        ngayt = now - timedelta(days=x)
        obs = ['12', '00']
        for zz in obs:
            file_path = '/Transmit/DuBaoDiem/TTB/' + ngayt.strftime('%Y%m%d') + zz  # Đường dẫn tới file trên máy chủ FTP
            # Kết nối và đọc file từ máy chủ FTP
            with FTP(ftp_host) as ftp:
                ftp.login(user=ftp_user, passwd=ftp_password)
                try:
                    ftp.cwd(file_path)
                    # files = ftp.nlst(file_path)
                    if ftp.nlst(tram):
                        with open(tram, 'wb') as file:
                            ftp.retrbinary('RETR ' + tram, file.write)
                        
                        with open(tram, 'r', encoding='utf-8') as file:
                            cnten = file.read()
                            found_file = True
                            break  # Thoát vòng lặp trong trường hợp tìm thấy file
                except:
                    pass
    # print(cnten)
    vt_ll =cnten.index('Lat,')
    first_line = cnten[:vt_ll]
    cnten = cnten[cnten.index('FORECAST'):]

    pp = first_line.split(" ")
    gio = int(pp[8].replace('\n',''))
    ngay_tt = int(pp[7].replace('\n',''))
    thang = int(pp[6].replace('\n',''))
    nam = int(pp[5].replace('\n',''))
    
    mohinh = pd.read_csv(io.StringIO(cnten), delimiter=r"\s+")
    mohinh = mohinh.astype(float)
   
    bd=datetime(nam,thang,ngay_tt,gio) + timedelta(hours=7)
    # print(bd)
    mohinh.insert(0,'time',pd.date_range(bd, periods=len(mohinh['FORECAST']), freq="6H"))
    mohinh['huong'] = np.degrees(np.arctan2(mohinh['USRF(m/s)'], mohinh['VSRF(m/s)']))
    mohinh['huong'] = mohinh['huong'].apply(convert_direction)
    mohinh['huong'] = mohinh['huong'].apply(lambda x: map_wind_direction(x))
    mohinh['wind_speed'] =round(np.sqrt(mohinh['USRF(m/s)']**2 + mohinh['VSRF(m/s)']**2),1)
    ngaytruoc = ngay + timedelta(hours=tg_db)
    mohinh = mohinh[(mohinh['time'] >= ngay) & (mohinh['time']<=ngaytruoc)]
    # print(mohinh)
    muadb = mohinh['RAIN6(mm/6h)'].sum()
    # sxm = mohinh['PoP(%)'].max()
    txmax = mohinh['TSRF(T)'].max()
    txmin = mohinh['TSRF(T)'].min()
    tnmax = mohinh['TTDSRF(T)'].max()
    tnmin = mohinh['TTDSRF(T)'].min()
    huonggio = mohinh['huong'].value_counts().idxmax()
    vmax = mohinh['wind_speed'].max()
    vmin = mohinh['wind_speed'].min()
    doamax = mohinh['RHSRF(%)'].max()
    doamin = mohinh['RHSRF(%)'].min()
    # print(ngay)
    # print(mohinh)
    return muadb,txmax,txmin,tnmax,tnmin,huonggio,vmax,vmin,doamax,doamin
# print(read_ecmwf(datetime(2023,8,8,7),'BaDon.txt',48))

# print(read_raii(datetime(2023,8,8,7),48))
def read_muadb_sever_sontranh(tg_db,tenho):
    hostname = '203.209.181.171'
    port = 22
    username = 'mpi'
    password = 'mpi@1234'
    # Tạo kết nối SSH
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password)
    # Đường dẫn tới tệp tin .txt trên máy chủ
    tg = datetime.now()
    # tg = (ngay - timedelta(days=1)).strftime('%d%m%Y')
    obs = ['12', '00']
    ngaylayfile = [tg,tg-timedelta(days=1)]
    for ngay in ngaylayfile:
        for zz in obs:        
            try:
                remote_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_36h/QuangNam_{}z_3k36h.txt'.format(zz,zz)
                # print(remote_file_path)
                # Đọc nội dung của tệp tin từ máy chủ
                sftp = client.open_sftp()
                remote_file = sftp.open(remote_file_path)
                file_contents = remote_file.read().decode()
                break
            except:
                pass
    
    # print(file_contents)
    # Đóng kết nối SSH
    remote_file.close()
    sftp.close()
    client.close()
    df = pd.read_csv(io.StringIO(file_contents), delimiter=r"\s+")
    df = df[1:]
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]
    if tenho =='SÔNG TRANH 2':
        df =df[['TraBui(ST2)','TraCang(ST2)','TraDon(ST2)','TraGiac(ST2)','TraLeng(ST2)','TraLinh(ST2)','TraMai(ST2)','UBNDNTM(ST2)','Dap(ST2)','TraNam2(ST2)','TraVan(ST2)']]
        df.columns = ['Trà Bui','Trà Cang','Trà Dơn','Trà Giác','Trà Leng','Trà Linh','Trà Mai','UBNDNTM','Đập chính','Trà Nam','Trà Vân']
    elif tenho =='A VƯƠNG':
        df =df[['TraBui(ST2)','TraCang(ST2)','TraDon(ST2)','TraGiac(ST2)','TraLeng(ST2)','TraLinh(ST2)','TraMai(ST2)','UBNDNTM(ST2)','Dap(ST2)','TraNam2(ST2)','TraVan(ST2)']]
        # name_viet = ['Đập tràn A Vương','UBND Ab Vương','Đồn biên phòng A Nông','UBND Huyện Tây Giang','UBND Xã Dang','Trạm Xã A Tep','Trạm Xã A Rooi','Trạm UBND Xã Blahee']
        # df.columns = name_viet
    elif tenho =='SÔNG BUNG 2':
        df =df[['DapSBung2','TrHySBung2','NMSongBung2','GaRiSBung2']]
        df.columns = ['Đập SB2','TrHy','Chơm','A Xan']
    elif tenho =='SÔNG BUNG 4':
        df =df[['DonBQNGiang','ChaVaNMDHSB4','DapSBung4','ZuoihSBung4','TrHySBung2','LaDeeSBung4','CuakhauNG']]
        df.columns = ['ĐăkPring','Chalval','Đầu mối','Zuôi','TrHy','LaDee','Đak Ốc']
        
    df.dropna(inplace=True)
    df = df.reset_index(drop=True)
    
    first_line = file_contents[:file_contents.index('Time')-1]
    pp = first_line.split(" ")
    ngaythangnam = pp[-1].replace('\n','')
    gio = pp[-3].replace('h','')
    tgbd  = datetime.strptime(ngaythangnam + " " + gio, "%d-%m-%Y %H") + timedelta(hours=3)
    df.insert(0,'time',pd.date_range(tgbd,periods=(df.shape[0]),freq='3h'))
    df = df[(df['time']>= datetime.now()) & (df['time']<= datetime.now() + timedelta(hours=tg_db))]
    # print(df)
    df.iloc[:,1:] = df.iloc[:,1:].astype(float)
    df =df.iloc[:,1:].sum()
    df = df.to_frame().T
    return df
def read_gio_sever_sontranh(tg_db):
    hostname = '203.209.181.171'
    port = 22
    username = 'mpi'
    password = 'mpi@1234'
    # Tạo kết nối SSH
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password)
    # Đường dẫn tới tệp tin .txt trên máy chủ
    tg = datetime.now()
    obs = ['12', '00']
    ngaylayfile = [tg,tg-timedelta(days=1)]
    for ngay in ngaylayfile:
        for zz in obs:        
            try:
                remote_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_36h/QuangNam_{}z_3k36h.txt'.format(zz,zz)
                # print(remote_file_path)
                # Đọc nội dung của tệp tin từ máy chủ
                sftp = client.open_sftp()
                remote_file = sftp.open(remote_file_path)
                file_contents = remote_file.read().decode()
                break
            except:
                pass
    
    # print(file_contents)
    # Đóng kết nối SSH
    remote_file.close()
    sftp.close()
    client.close()
    df = pd.read_csv(io.StringIO(file_contents), delimiter=r"\s+")
    df = df[1:]
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]
    df =df[['TraBui(ST2)','TraCang(ST2)','TraDon(ST2)','TraGiac(ST2)','TraLeng(ST2)','TraLinh(ST2)','TraMai(ST2)','UBNDNTM(ST2)','Dap(ST2)','TraNam2(ST2)','TraVan(ST2)']]
    df.columns = ['Trà Bui','Trà Cang','Trà Dơn','Trà Giác','Trà Leng','Trà Linh','Trà Mai','UBNDNTM','Đập chính','Trà Nam','Trà Vân']

    df.dropna(inplace=True)
    df = df.reset_index(drop=True)
    
    first_line = file_contents[:file_contents.index('Time')-1]
    pp = first_line.split(" ")
    ngaythangnam = pp[-1].replace('\n','')
    gio = pp[-3].replace('h','')
    tgbd  = datetime.strptime(ngaythangnam + " " + gio, "%d-%m-%Y %H") + timedelta(hours=3)
    df.insert(0,'time',pd.date_range(tgbd,periods=(len(df['Trà Bui'])),freq='3h'))
    df = df[(df['time']>= datetime.now()) & (df['time']<= datetime.now() + timedelta(hours=tg_db))]
    # print(df)
    df.iloc[:,1:] = df.iloc[:,1:].astype(float)
    df =df.iloc[:,1:].sum()
    df = df.to_frame().T
    return df
# read_muadb_sever(datetime.now())
# read_raii(datetime(2023,6,24),72)

def anh_mo_hinh_WRF():
    hostname = '203.209.181.171'
    port = 22
    username = 'mpi'
    password = 'mpi@1234'
    # Tạo kết nối SSH
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password)
    # Đường dẫn tới tệp tin .txt trên máy chủ
    tg = datetime.now()
    obs = ['12', '00']
    ngaylayfile = [tg,tg-timedelta(days=1)]
    for ngay in ngaylayfile:
        for zz in obs:
            try:   
                sftp = client.open_sftp()
                image_nhiet_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_72h/Luoi1/NhietL1_13.png'.format(zz,zz) 
                image_nhiet_file = sftp.open(image_nhiet_file_path,'rb')
                image_nhiet_data = image_nhiet_file.read()
                image_nhiet = Image.open(io.BytesIO(image_nhiet_data))
                
                image_gio_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_72h/Luoi1/Gio10m_13.png'.format(zz,zz) 
                image_gio_file = sftp.open(image_gio_file_path,'rb')
                image_gio_data = image_gio_file.read()
                image_gio = Image.open(io.BytesIO(image_gio_data))
                
                image_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_72h/Luoi1/AmApL1_13.png'.format(zz,zz) 
                image_file = sftp.open(image_file_path,'rb')
                image_data = image_file.read()
                image_amap = Image.open(io.BytesIO(image_data))

                image_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_72h/Luoi1/MayL1_13.png'.format(zz,zz) 
                image_file = sftp.open(image_file_path,'rb')
                image_data = image_file.read()
                image_may = Image.open(io.BytesIO(image_data))                
            except:
                pass
    sftp.close()
    client.close()
    return image_gio,image_nhiet,image_amap,image_may
        

