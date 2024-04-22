import paramiko
from datetime import datetime,timedelta
import pandas as pd
import io
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
    thoat = False
    for ngay in ngaylayfile:
        if thoat==True:
            break
        for zz in obs:        
            try:
                if tenho !='A VƯƠNG':
                    remote_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/Hinh_{}z_36h/QuangNam_{}z_3k36h.txt'.format(zz,zz)
                else:
                    remote_file_path = '/home/disk2/KQ_WRF72h/' + ngay.strftime('%d%m%Y') + '/{}z/TTB_{}z_36h.txt'.format(zz,zz)
                    thoigianbatdau = datetime(ngay.year,ngay.month,ngay.day,int(zz))
                    # print(thoigianbatdau)
                # print(remote_file_path)
                # Đọc nội dung của tệp tin từ máy chủ
                sftp = client.open_sftp()
                remote_file = sftp.open(remote_file_path)
                file_contents = remote_file.read().decode()
                thoat = True
                break
            except:
                pass
    
    # print(file_contents)
    # Đóng kết nối SSH
    remote_file.close()
    sftp.close()
    client.close()
    df = pd.read_csv(io.StringIO(file_contents), delimiter=r"\s+")
    if tenho !='A VƯƠNG':
        df = df[1:]
        df = df.T
        df.columns = df.iloc[0]
        df = df[1:]
    else:
        # df = df[1:]
        df = df.T
        df.columns = df.iloc[0]
        df = df[1:]
        # print(df)
        # print(df.T)
    if tenho =='SÔNG TRANH 2':
        df =df[['TraBui(ST2)','TraCang(ST2)','TraDon(ST2)','TraGiac(ST2)','TraLeng(ST2)','TraLinh(ST2)','TraMai(ST2)','UBNDNTM(ST2)','Dap(ST2)','TraNam2(ST2)','TraVan(ST2)']]
        df.columns = ['Trà Bui','Trà Cang','Trà Dơn','Trà Giác','Trà Leng','Trà Linh','Trà Mai','UBNDNTM','Đập chính','Trà Nam','Trà Vân']
    elif tenho =='A VƯƠNG':
        # print(df)
        df = df.reset_index(False)
        # df =df[['TraBui(ST2)','TraCang(ST2)','TraDon(ST2)','TraGiac(ST2)','TraLeng(ST2)','TraLinh(ST2)','TraMai(ST2)','UBNDNTM(ST2)','Dap(ST2)','TraNam2(ST2)','TraVan(ST2)']]
        df = df[['AV1','AV2','AV3','AV4','AV5','AV6','HIEN']]
        # name_viet = ['Đập tràn A Vương','UBND Ab Vương','Đồn biên phòng A Nông','UBND Huyện Tây Giang','UBND Xã Dang','Trạm Xã A Tep','Trạm Xã A Rooi','Trạm UBND Xã Blahee']
        df.columns = ['Đập tràn A Vương','UBND Ab Vương','Đồn biên phòng A Nông','UBND Huyện Tây Giang','UBND Xã Dang','Trạm Xã A Tep','Hien']
    elif tenho =='SÔNG BUNG 2':
        df =df[['DapSBung2','TrHySBung2','NMSongBung2','GaRiSBung2']]
        df.columns = ['Đập SB2','TrHy','Chơm','A Xan']
    elif tenho =='SÔNG BUNG 4':
        df =df[['DonBQNGiang','ChaVaNMDHSB4','DapSBung4','ZuoihSBung4','TrHySBung2','LaDeeSBung4','CuakhauNG']]
        df.columns = ['ĐăkPring','Chalval','Đầu mối','Zuôi','TrHy','LaDee','Đak Ốc']
    
    if tenho !='A VƯƠNG':
        df.dropna(inplace=True)
        df = df.reset_index(drop=True)
        first_line = file_contents[:file_contents.index('Time')-1]
        pp = first_line.split(" ")
        ngaythangnam = pp[-1].replace('\n','')
        gio = pp[-3].replace('h','')
        tgbd  = datetime.strptime(ngaythangnam + " " + gio, "%d-%m-%Y %H") + timedelta(hours=3)
        df.insert(0,'time',pd.date_range(tgbd,periods=(df.shape[0]),freq='3h'))
    else:
        print(thoigianbatdau)
        df.insert(0,'time',pd.date_range(thoigianbatdau+ timedelta(hours=10),periods=(df.shape[0]),freq='3h')) 
    # print(df)
    df = df[(df['time']>= datetime.now()) & (df['time']<= datetime.now() + timedelta(hours=tg_db))]
    # print(df)
    df.iloc[:,1:] = df.iloc[:,1:].astype(float)
    df =df.iloc[:,1:].sum()
    df = df.to_frame().T
    return df
read_muadb_sever_sontranh(48,'A VƯƠNG')