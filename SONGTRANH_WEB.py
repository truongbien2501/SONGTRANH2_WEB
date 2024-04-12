import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader
from datetime import datetime,timedelta
from streamlit_extras.metric_cards import style_metric_cards
from func.MOHINH_SOTRI import read_muadb_sever_sontranh
import paramiko
from PIL import Image
import io
from ftplib import FTP
import PIL
import vincent
import json
from PIL import ImageFile
from streamlit_option_menu import option_menu
import base64
st.set_option('deprecation.showPyplotGlobalUse', False)

# Thêm nút tải dữ liệu
def download_csv(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
    return href

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
                break             
            except:
                pass
    sftp.close()
    client.close()
    return image_gio,image_nhiet,image_amap,image_may

def read_ftp_sever_image(tram):
        # Thông tin máy chủ FTP và đường dẫn đến file ftp://203.209.181.174/DAKDRINH/Image
        ftp_host = '113.160.225.111'
        ftp_user = 'kttvttbdb'
        ftp_password = '618778'
        file_path = '/Dulieu-Bantinkttvttb/5-Quang Ngai/LUU TRU/PHAN MEM/mobiapp' + '/' + tram
        # Kết nối đến máy chủ FTP
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)
        image_data = io.BytesIO()
        ftp.retrbinary('RETR ' + file_path, image_data.write)
        # Đóng kết nối FTP
        ftp.quit()
        # Chuyển dữ liệu ảnh thành đối tượng hình ảnh và trả về
        image_data.seek(0)
        anh = PIL.Image.open(image_data)
        return anh
    
@st.cache_data
def xulysolieu_mua(df):
    # print(df)
    # now = datetime.now()
    
    # print(df)
    df_xl = pd.DataFrame()
    # Lấy danh sách tên cột từ df1
    column_names = df.columns
    # Tạo DataFrame mới với các tên cột từ df1
    df_xl = pd.DataFrame(columns=column_names)
    
    #mua1h
    df_xl = pd.concat([df_xl, df.tail(1)])
    # print(df_xl.index)
    # df_xl.loc[0].values[0] = 'Mưa 1h qua'
    # # mưa2h
    mua2h =  df.rolling(2,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    # # mưa3h
    mua2h =  df.rolling(3,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    
    # # mưa4h
    mua2h =  df.rolling(4,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    # # mưa6h
    mua2h =  df.rolling(6,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    
    # # mưa12h
    mua2h =  df.rolling(12,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    # # mưa24h
    mua2h =  df.rolling(24,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    
    # # mưa48h
    mua2h =  df.rolling(48,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    
    # # mưa24h
    mua2h =  df.rolling(72,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
        
    # # mưa24h
    mua2h =  df.rolling(72+24,min_periods=1).sum()
    df_xl = pd.concat([df_xl, mua2h.tail(1)])
    
    df_xl.reset_index(drop=False,inplace=True)
    gt_dq = ['1h qua','2h qua','3h qua','4h qua','6h qua','12h qua','24h qua', '48h qua', '72h qua','4ngay qua']
    df_xl.insert(0,'Mưa đã qua',gt_dq)
    df_xl = df_xl.drop('index', axis=1)
    df_xl = df_xl.set_index('Mưa đã qua')
    df_xl = df_xl.applymap("{0:.1f}".format)
    df_xl = df_xl.T
    return df_xl
@st.cache_data
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
    # data = data.replace(0,np.nan)
    # data= data.interpolate(method='linear')
    # data = data.applymap("{0:.2f}".format)
    data.reset_index(drop=False,inplace=True)   

    
    df_mua = data.drop(['mucnuoc','qden','qxa','Giao Thuy','Nong Son','Cau Lau'],axis=1)
    data['mucnuoc'] =  data['mucnuoc'].map('{0:.2f}'.format)
    data['qden'] =  data['qden'].map('{0:.1f}'.format)
    data['qxa'] =  data['qxa'].map('{0:.1f}'.format)
    data.rename(columns={'time':'Thời gian','mucnuoc':'Mực nước (m)','qden':'Q đến (m3/s)','qxa':'Q điều tiết (m3/s)','Giao Thuy':'Giao Thủy','Nong Son':"Nông Sơn",'Cau Lau':'Câu Lâu'},inplace=True)
    # name_eng = ['TRABUI', 'tracang', 'tradon', 'tragiac', 'traleng', 'tralinh','TRAMAI', 'UBNDHnamTM', 'tramdapst2', 'tranam2', 'travan']
    name_viet = ['time','Trà Bui', 'Trà Cang', 'Trà Dơn', 'Trà Giác', 'Trà Leng', 'Trà Linh','Trà Mai', 'UBNDHnamTM', 'Trà Đốc(Đập chính)', 'Trà Nam', 'Trà Vân']
    df_mua.columns =name_viet
    data.iloc[:,1:7] = data.iloc[:,1:7].astype(float)
    return df_mua,data
@st.cache_data
def Mucnuoc_songtranh():
    now = datetime.now()
    kt = datetime(now.year,now.month,now.day,now.hour)
    bd = kt - timedelta(days=1)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='h')
    tram = pd.read_csv('TS_ID/TTB/songtranh3.txt')
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
    # data = data.dropna()
    return data['mucnuoc'].iloc[-1],data['qxa'].iloc[-1],data['qden'].iloc[-1]
@st.cache_data
def dubao_songtranh():
    kt = datetime(2024,1,25)
    bd = datetime(2024,1,25)
    data = pd.DataFrame()
    data['time'] = pd.date_range(bd,kt,freq='h')
    tram = pd.read_csv('TS_ID/TTB/dubao.txt')
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
    data.reset_index(drop=False,inplace=True)  
    return data    

# @st.cache_data
# def vebieudomua(df_mua):
#     # fig, ax = plt.subplots()

#     # # Điều chỉnh lề trên, dưới, trái và phải
#     # top_margin = 0.1  # Thay đổi lề trên (top margin)
#     # bottom_margin = 0.05  # Thay đổi lề dưới (bottom margin)
#     # left_margin = 0.05  # Thay đổi lề trái (left margin)
#     # right_margin = 0.1  # Thay đổi lề phải (right margin)
#     # ax.figure.subplots_adjust(top=top_margin, bottom=bottom_margin, left=left_margin, right=right_margin)
    
#     luongmua = df_mua.iloc[:,1:].sum().to_list()
#     tram= df_mua.columns.to_list()[1:]
#     print(tram)
#     # print(tram,luongmua)
#     fig, ax = plt.subplots(figsize=(5, 4))
#     ax.bar(tram,luongmua)
#     ax.set_xlabel('Trạm',size = 20)
#     ax.set_ylabel('Lượng mưa (mm)',size = 20)
#     ax.set_title('Biểu đồ mưa',size = 30)
#     # ax2.legend(ghichu, loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=len(ghichu))
#     # ax2.legend(ghichu)
#     # ax2.grid(True,linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
#     # ax2.set_facecolor((1.0, 1.00, 0.196, 0.5)) 
#     plt.xticks(rotation=90, size=10)
#     plt.yticks(rotation=0, size=10)
#     # plt.tight_layout(pad=1)
#     # plt.show()
#     return fig,ax
@st.cache_data
def html_mua(df,tentram):
    # print(df)
    df = df.replace('nan','0.0')
    # print(df)
    html = f"""
    <h1 ><span style="color:black;">{tentram}</span></h1>
    <ul style="background-color: lightblue;">
    <li style="color:black;">Lượng mưa 1h qua: {df['1h qua']}mm</li>
    <li style="color:black;">Lượng mưa 2h qua: {df['2h qua']}mm</li>
    <li style="color:black;">Lượng mưa 3h qua: {df['3h qua']}mm</li>
    <li style="color:black;">Lượng mưa 4h qua: {df['4h qua']}mm</li>
    <li style="color:black;">Lượng mưa 6h qua: {df['6h qua']}mm</li>
    <li style="color:black;">Lượng mưa 12h qua: {df['12h qua']}mm</li>
    <li style="color:black;">Lượng mưa 24h qua: {df['24h qua']}mm</li>  
    <li style="color:black;">Lượng mưa 48h qua: {df['48h qua']}mm</li>
    <li style="color:black;">Lượng mưa 72 qua: {df['72h qua']}mm</li>             
    </ul>
    """
    
    if float(df['24h qua'])>=50:
        canhbaodo = "red"
    elif float(df['24h qua'])>20 and float(df['24h qua'])<50:
        canhbaodo = "yellow"
    else:
        canhbaodo = "green"
    html1=f"""
                <div><svg>
                    <circle cx="30" cy="30" r="20" fill="#69b3a2" opacity=".3"/>
                    <circle cx="30" cy="30" r="10" fill="{canhbaodo}", opacity=".1.5" 
                </svg></div>"""
    return html,html1
@st.cache_data
def graphs_mua(df):
    bd = df['time'].min()
    kt = df['time'].max()
    # print(bd)
    #ve mua
    luongmua = df.iloc[:,1:].sum().to_list()
    tram= df.columns.to_list()[1:]
    investment_by_business_type= pd.DataFrame(data={'Trạm':tram,'Lượng mưa':luongmua})
    fig_mua=px.bar(
       investment_by_business_type,
       x="Trạm",
       y='Lượng mưa',
       orientation="v",
       title="<b>Biểu đồ mưa thực đo từ {} đến {}</b>".format(bd.strftime('%Hh %d/%m'),kt.strftime('%Hh %d/%m')),
       color_discrete_sequence=["#0083B8"],
       template="plotly_white",
    )
    fig_mua.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
     )
    return fig_mua
@st.cache_data
def graphs_mua_db(df):
    # print(df)
    #ve mua
    luongmua = df.sum().to_list()
    tram= df.columns.to_list()
    investment_by_business_type= pd.DataFrame(data={'Trạm':tram,'Lượng mưa':luongmua})
    fig_mua_db=px.bar(
       investment_by_business_type,
       x="Trạm",
       y='Lượng mưa',
       orientation="v",
       title="<b> Biểu đồ mưa dự báo lưu vực 24h tới</b>",
       color_discrete_sequence=["#0083B8"],
       template="plotly_white",
       color=investment_by_business_type['Lượng mưa'],
       color_continuous_scale='Rainbow',
    )
    fig_mua_db.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
     )
    return fig_mua_db
@st.cache_data
def graphs_h(df_h):
    # # vẽ muc nuoc
    fig_mucnuoc=px.line(df_h,x=df_h.columns.to_list()[0],y="Mực nước (m)",
       orientation="v",
       title="<b>Đường quá trình mực nước hồ Sông Tranh 2</b>",
       color_discrete_sequence=["#0083b8"],
       template="plotly_white",
    )
    fig_mucnuoc.update_traces(mode="lines")
    fig_mucnuoc.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig_mucnuoc.update_yaxes(showspikes=True, spikecolor="orange", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig_mucnuoc.update_layout(spikedistance=1000, hoverdistance=100)
    # fig_mucnuoc.update_layout(
    # xaxis=dict(tickmode="linear"),
    # plot_bgcolor="rgba(0,0,0,0)",
    # yaxis=(dict(showgrid=True))
    #  )
    return fig_mucnuoc
# @st.cache_resource
# def graphs_h_tv(df_h,tentram,namesave):
#     # # vẽ muc nuoc
#     fig_mucnuoc=px.line(df_h,x=df_h.columns.to_list()[0],y=tentram,
#        orientation="v",
#        title="<b>Đường quá trình mực nước tram {}</b>".format(tentram),
#        color_discrete_sequence=["#0083b8"],
#        template="plotly_white",
#     )
#     fig_mucnuoc.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=True))
#      )
#     # fig_mucnuoc.show()
#     fig_mucnuoc.write_html("data/{}.html".format(namesave))  
@st.cache_resource
def graphs_Q(df_Q):
    # Vẽ biểu đồ
    fig = px.line(df_Q, x = 'Thời gian' ,y=[df_Q['Q đến (m3/s)'],df_Q['Q điều tiết (m3/s)']],color_discrete_sequence=['Black', 'Red'])
    fig.update_traces(mode="lines")
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="orange", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)
    # Cập nhật layout của biểu đồ
    fig.update_layout(
        title="<b>Đường quá trình thực đo lưu lượng</b>",
        xaxis=dict(tickmode="linear",tickformat="%d-%m-%Y %H:%M",dtick="H1",tickangle=-60),
        plot_bgcolor="rgba(1,0,0,0)",
        yaxis=dict(showgrid=True,title="Lưu lượng (m3/s)"),
        legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

@st.cache_resource
def html_mucnuoc(df,tentram,tram_anh):
    mucnuocne = df[['Thời gian',tentram]]
    # print(mucnuocne[tentram].values[-1])
    # df = df.replace('nan','0.0')
    html = f"""
    <body style="background-color: white;">
    <h1 ><span style="color:black;">{tentram} <br> Mực nước: {mucnuocne[tentram].values[-2]} m</span></h1>
    <iframe src="data/{tram_anh}.html" height="200" width="300" title="Iframe Example"></iframe>
    <body>
    """
    return html
@st.cache_resource
def read_ftp_sever_rada_image():
    # Your SSH details
    host = '113.161.6.128'
    port = 2233
    username = 'radarop'
    password = 'xxxxxx'
    remote_directory = '/usr/iris_data/jpg'

    # Create SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, password=password)

    # Create SFTP connection
    sftp = client.open_sftp()
    filenames = sftp.listdir(remote_directory)
    # print(filenames)
        # Get the latest filename
    latest_filename = sorted(filenames)[-1]

    # Open the image file directly from SFTP
    remote_filepath = f'{remote_directory}/{latest_filename}'
    image_file = sftp.open(remote_filepath, 'r')

    # Ensure Pillow can handle incomplete images
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # Open the image using Pillow
    image = PIL.Image.open(image_file)

    # Close connections
    # image_file.close()
    # sftp.close()
    # client.close()

    return image
# Thiết lập kích thước và chế độ hiển thị trang ứng dụng
# st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="KTTV TTB", page_icon="	:sun_behind_rain_cloud:")
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Hồ chứa KTTV TTB", page_icon="	:sun_behind_rain_cloud:")
with open("CSS/styles.css",'r',encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# tao form dang nhap
with open(r'login\list_uer.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
# print(authenticator)
name, authentication_status, username = authenticator.login('Login', 'main')
# print(name)
# print(username)
# print(authentication_status)
if authentication_status == False:
    st.warning('Không đúng tên hoặc mật khẩu')
elif authentication_status == None:
    st.warning('Nhập tên và mật khẩu')
elif authentication_status == True:
    def hochua_quangnam():
        # st.title("ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ\nĐIỀU HÀNH HỒ CHỨA") # tạo tiêu đề
        custom_css = """
            <style>
                h1 {
                    font-size: 50;
                    color: Blue;
                    font-family: 'Times New Roman';
                    text-align: center;
                    
                }
                .logo {
                    max-width: 100px; /* Điều chỉnh kích thước logo theo nhu cầu */
                }
            </style>
        """
        # Sử dụng st.markdown để hiển thị HTML và CSS
        # st.markdown(custom_css, unsafe_allow_html=True)
        # st.markdown('<h1>Trang Chủ</h1>', unsafe_allow_html=True)
        st.markdown('<h1>ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ</h1>', unsafe_allow_html=True)
        # st.markdown(f'<img class="logo" src="{logo_image}">', unsafe_allow_html=True)
        # st.markdown(f'<img class="banner" src="{banner_image}">', unsafe_allow_html=True)
        # st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
        # st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">ĐÀI KHÍ TƯỢNG THUỶ VĂN TỈNH QUẢNG NGÃI</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
        # st.write('----------------------------')

        # load muc nuoc
        h_songtranh2,qxa_ht,qden_ht = Mucnuoc_songtranh()
        data_dubao = dubao_songtranh()
        array_data = np.genfromtxt('TS_ID/H_W.txt', delimiter=",",names=True,encoding=None)
        row_index = np.where(array_data['H']==float(h_songtranh2))
        dungtich_songtranh2 = str(array_data['W'][row_index])[1:-1]
        tyle = (float(dungtich_songtranh2)/733.4)*100
        # tinh dung tich cac ho chua
        data = {"Hồ": ["Sông Tranh", "A Vương", "Sông Bung 2"],
                "Mực nước(m)": ['{:.1f}'.format(h_songtranh2), '375.25', '597.86'],
                "Dung tích (tr/m3)": [dungtich_songtranh2, "-", "-"],
                "Tỷ lệ(%)": ['{:.1f}'.format(tyle), '-', "-"],
                "MNDBT": ['175', '380', '605'],
                "MN_CHẾT": ['145', '340', '565']
                }

        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(data)
        st.dataframe(df,use_container_width=True)

        # Tạo hộp văn bản và lấy giá trị người dùng nhập vào
        bd,bd_gio, kt,kt_gio = st.columns(4)
        # bd_gio, kt_gio = st.columns(2)

        ngaybd = bd.date_input("Ngày bắt đầu",value=datetime((datetime.now() - timedelta(days=5)).year,(datetime.now() - timedelta(days=5)).month,(datetime.now() - timedelta(days=5)).day))
        gio_batdau = bd_gio.time_input('Giờ bắt đầu',value=datetime.strptime("23:00", "%H:%M"))
        
        # Định dạng CSS tùy chỉnh cho phần tử date input
        custom_css = """
        <style>
            /* Thêm CSS tùy chỉnh cho phần tử date input */
            .st-ec {
                background-color: lightblue; /* Màu nền */
                color: black; /* Màu chữ */
                border: 2px solid lightblue; /* Viền */
                border-radius: 5px; /* Góc bo tròn */
            }
        </style>
        """
        # Nhúng mã CSS tùy chỉnh vào ứng dụng
        st.markdown(custom_css, unsafe_allow_html=True)

        # Định dạng CSS tùy chỉnh cho phần tử date input
        custom_css = """
        <style>
            /* Thêm CSS tùy chỉnh cho date input */
            .st-bu {
                background-color: #ffcc00; /* Màu nền */
                color: #000; /* Màu chữ */
                border: 2px solid #ffcc00; /* Viền */
                border-radius: 50px; /* Góc bo tròn */
            }
        </style>
        """
        # # Nhúng mã CSS tùy chỉnh vào ứng dụng
        st.markdown(custom_css, unsafe_allow_html=True)
        # Trong cột thứ hai, tạo lịch để chọn ngày kết thúc
        ngaykt = kt.date_input("Ngày kết thúc",value=datetime(datetime.now().year,datetime.now().month,datetime.now().day,datetime.now().hour))
        gio_ketthuc = kt_gio.time_input('Giờ kết thúc',value=datetime.strptime(datetime.now().strftime("%H:00"),"%H:00"))
    
        data_mua,solieu_hq = Bieudo_Q_H(datetime.combine(ngaybd, gio_batdau),datetime.combine(ngaykt, gio_ketthuc))
        # data_mua.iloc[:,1:] = 
        # print(data_mua)
        
        data_tichluy =  data_mua.set_index('time')
        data_tichluy = xulysolieu_mua(data_tichluy) # tinh mua 1h,3h,24h.....
        # print(data_tichluy.loc['Trà Đốc(Đập chính)']['24h qua'])
        total1,total2,total3,total4,total5,total6,total7=st.columns(7,gap='small')
        with total1:
            st.info('Hmax',icon="⭐")
            st.metric(label="Mực nước (m)",value=f"{solieu_hq['Mực nước (m)'].max():,.1f}")
        with total2:
            st.info('Htb',icon="⭐")
            st.metric(label="Mực nước (m)",value=f"{solieu_hq['Mực nước (m)'].mean():,.1f}")

        with total3:
            st.info('Qmax',icon="⭐")
            st.metric(label="Q đến hồ (m3/s)",value=f"{solieu_hq['Q đến (m3/s)'].max():,.1f}")

        with total4:
            st.info('Qtb',icon="⭐")
            st.metric(label="Q đến hồ tb (m3/s)",value=f"{solieu_hq['Q đến (m3/s)'].mean():,.1f}")
            
        with total5:
            st.info('Qxa',icon="⭐")
            st.metric(label="Q điều tiết (m3/s)",value=f"{solieu_hq['Q điều tiết (m3/s)'].max():,.1f}")
            
        with total6:
            st.info('Qxa',icon="⭐")
            st.metric(label="Q điều tiết tb (m3/s)",value=f"{solieu_hq['Q điều tiết (m3/s)'].mean():,.1f}")
        with total7:
            st.info('Qtbdb 24h',icon="⭐")
            st.metric(label="Qtb dự báo(m3/s)",value=data_dubao['qdb'].loc[0])
        style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
        
        
        with st.expander("VIEW SỐ LIỆU MỰC NƯỚC - LƯU LƯỢNG"):
            showData=st.multiselect('Filter: ',solieu_hq.iloc[:,:7].columns,default=solieu_hq.iloc[:,:7].columns.tolist())
            st.dataframe(solieu_hq[showData],use_container_width=True)
            if st.button('Tải dữ liệu H-Q'):
                st.markdown(download_csv(solieu_hq[showData]), unsafe_allow_html=True)

        left, right = st.columns(2)  
        left.plotly_chart(graphs_h(solieu_hq[['Thời gian','Mực nước (m)']]),use_container_width=True)
        right.plotly_chart(graphs_Q(solieu_hq),use_container_width=True)

        # print(data_tichluy)
        with st.expander("VIEW SỐ LIỆU MƯA"):
            showData=st.multiselect('Filter: ',data_mua.columns,default=data_mua.columns.tolist()[1:])
            st.dataframe(data_tichluy.loc[showData].replace('nan','0.0'),use_container_width=True)
            if st.button('Tải dữ liệu mưa'):
                st.markdown(download_csv(data_tichluy.loc[showData].replace('nan','0.0')), unsafe_allow_html=True)
                
        # components.html(data_mua.to_html())

        vemua,muadb = st.columns(2)    
        tramve = data_mua[['time'] + showData]
        # print(tramve)
        # images,ax =  vebieudomua(tramve)    
        vemua.plotly_chart(graphs_mua(tramve),use_container_width=True)
        muadubao= read_muadb_sever_sontranh(24)
        muadb.plotly_chart(graphs_mua_db(muadubao),use_container_width=True)
        
        try:
            image_gio,image_nhiet,image_amap,image_may = anh_mo_hinh_WRF()
            gio,nhiet = st.columns(2)
            gio.image(image_gio,use_column_width=True)
            nhiet.image(image_nhiet  ,use_column_width=True)        
            amap,may = st.columns(2)
            amap.image(image_amap,use_column_width=True)
            may.image(image_may,use_column_width=True)
            # may.image(read_ftp_sever_rada_image(),use_column_width=True)
        except:
            pass
        
        # Danh sách các điểm
        tram_kttv = {'Câu Lâu': (15.857806467135058, 108.27289741859273),
                    'Giao Thủy': (15.846, 108.109),
                    'Nông Sơn':(15.70276202116165, 108.03392429139377),
                    'Trà Đốc(Đập chính)': (15.331688, 108.147511),
                    'Trà Bui': (15.34661, 108.041526),
                    'Trà Giác': (15.240458, 108.178398),
                    'Trà Dơn': (15.243961, 108.0858880),
                    'Trà Leng': (15.272192, 108.014046),
                    'Trà Mai': (15.1547, 108.1085),
                    'Trà Cang': (15.1046490, 108.0714240),
                    'Trà Vân': (15.1130910, 108.1800410),
                    'Trà Nam': (14.9871600, 108.1336140),
                    'Trà Linh': (15.030926, 108.0241060),              
                    'Quần đảo Hoàng Sa(Việt Nam)': (16.6,112.7),
                    'Quần đảo Trường Sa(Việt Nam)': (9.45,112.904)
                    }
        # Tạo bản đồ Quảng Ngãi
        m = folium.Map(location=[15.3371600,108.39232], 
                        zoom_start=9,
                        width='95%',  # Định dạng kích thước chiều rộng
                        height='100%'  # Định dạng kích thước chiều cao
                    )
        # load lưu vuc len map    
        with open('data/SongTranh2.json', 'r') as f:
            data_json = json.load(f)
        folium.GeoJson(data=data_json, name='geometry',    
                    style_function=lambda feature: {
                        'fillColor': 'green',  # Chọn màu sắc ở đây
                        'color': 'black',
                        'weight': 2,
                        'fillOpacity': 0.5,}).add_to(m)
        # Tạo các điểm Marker với Tooltip và thay đổi màu sắc
        for location, coord in tram_kttv.items():
            if 'Câu Lâu' in location or 'Giao Thủy' in location or 'Nông Sơn' in location: # bieu tuong thuy chi cho tram do thuy van
                name_en = ['caulau','giaothuy','nongson']
                name_vi = ['Câu Lâu','Giao Thủy','Nông Sơn']
                
                # graphs_h_tv(solieu_hq,location,name_en[name_vi.index(location)])
                custom_icon = folium.CustomIcon(icon_image="image/thuychi.png", icon_size=(10, 50))
                # html = html_mucnuoc(solieu_hq,location,name_en[name_vi.index(location)])
                # iframe = folium.IFrame(html=html, width=300, height=300)
                # popup = folium.Popup(iframe, max_width=2650)
                # folium.Marker(coord,popup=popup,icon=custom_icon).add_to(m)

                line_map = vincent.Line(solieu_hq[location].to_list(),height=100, width=200)
                line_map.axis_titles(x='Date',y='H (m)') 
                line_map.legend(title=location)
                data = json.loads(line_map.to_json())
                marker = folium.Marker(coord,icon=custom_icon).add_to(m)
                popup = folium.Popup(max_width=300).add_to(marker)
                folium.Vega(data, width="50%", height="50%").add_to(popup)
            elif 'Trà Đốc' in location: # bieu tuong thuy chi cho tram do thuy van
                custom_icon = folium.CustomIcon(icon_image="image/songtranh.jpg", icon_size=(50, 70))
                thongso = pd.read_csv('data/songtranh2.csv')
                thongso = thongso[['Thông số','Sông Tranh 2','Đơn vị']]
                thongso.loc[thongso['Thông số'] == 'Mực nước', 'Sông Tranh 2'] = h_songtranh2
                thongso.loc[thongso['Thông số'] == 'Q đến', 'Sông Tranh 2'] = qden_ht
                thongso.loc[thongso['Thông số'] == 'Q điều tiết', 'Sông Tranh 2'] = qxa_ht
                thongso.loc[thongso['Thông số'] == 'Q dự báo 24h', 'Sông Tranh 2'] = data_dubao['qdb'].loc[0]
                thongso.loc[thongso['Thông số'] == 'Tỷ lệ hữu ích', 'Sông Tranh 2'] = '{:.1f}'.format(tyle)       
                html = thongso.to_html(classes="table table-striped table-hover table-condensed table-responsive")
                popup = folium.Popup(html=html, max_width=2650)
                folium.Marker(coord,popup=popup,icon=custom_icon).add_to(m)
                # folium.Marker(coord, popup=location,icon=folium.Icon(color='blue')).add_to(m)            
            elif 'Việt Nam' not in location:
                # # custom_icon = folium.CustomIcon(icon_image="image/mua.jpg", icon_size=(30, 30)) # bieu tuong mua cho tram do mua
                # data_tichluy_html = data_tichluy.loc[location]
                # print(data_tichluy_html)
                # hlm,hlm1 = html_mua(data_tichluy_html,location)
                # iframe = folium.IFrame(html=hlm, width=300, height=300)
                # popup = folium.Popup(iframe, max_width=2650)
                # folium.Marker(coord,popup=popup,icon=folium.DivIcon(html=hlm1)).add_to(m)
                
                custom_icon = folium.CustomIcon(icon_image="image/mua.jpg", icon_size=(30, 30)) # bieu tuong mua cho tram do mua
                data_tichluy_html = data_tichluy.loc[location]
                # print(data_tichluy_html)
                data_tichluy_html = pd.DataFrame(data_tichluy_html).replace('nan','0.0')
                html = data_tichluy_html.to_html(classes="table table-striped table-hover table-condensed table-responsive")
                popup = folium.Popup(html=html, max_width=2650)
                folium.Marker(coord,popup=popup,icon=custom_icon).add_to(m)
            else:
                custom_icon = folium.CustomIcon(icon_image="image/quocky.png", icon_size=(50, 70))
                folium.Marker(coord, popup=location,icon=custom_icon).add_to(m)
                
        # # Hiển thị bản đồ trong ứng dụng Streamlit
        # Tạo expander cho Dự báo và Kết quả

        # Tạo bố cục gồm 2 cột và 2 hàng
        col1, col2 = st.columns(2)
        st.markdown(
        """
        <style>
            /* Tùy chỉnh CSS cho phần mở rộng */
            .streamlit-expanderHeader {
                background-color: #3399ff; /* Màu nền phần mở rộng */
                color: #00008b; /* Màu chữ phần mở rộng */
            }
            .streamlit-expanderContent {
                padding: 10; /* Khoảng cách giữa nội dung phần mở rộng */
            }
            
            /* Tùy chỉnh CSS cho hộp chọn */
            .streamlit-selectbox select {
                background-color: #ffcc00; /* Màu nền hộp chọn */
                color: #ff8c00; /* Màu chữ hộp chọn */
                border: 2px solid #ffcc00; /* Viền của hộp chọn */
                border-radius: 50px; /* Góc bo tròn của hộp chọn */
            }
        </style>
        """,
        unsafe_allow_html=True
    )
        with col1:
            with st.expander ("Bản tin dự báo"):
                # placeholder = st.text_input("Chọn loại bản tin", "Mời chọn tin", key="placeholder")
                tin_loai = st.selectbox("Chọn loại bản tin", ["Xin mời chọn.....","Hạn ngắn", "Hạn vừa", "Tin Lũ"])
                # tin_loai = custom_selectbox("Chọn loại bản tin", ["Mời chọn tin","Hàng ngày", "10 ngày", "LULU"])
                if tin_loai == "Hạn ngắn":
                    images =   read_ftp_sever_image('tin_TVHN.png')
                    st.image(images,use_column_width=True)
                elif tin_loai == "Hạn vừa":
                    images =   read_ftp_sever_image('tin_TVHV.png')
                    st.image(images,use_column_width=True)
                elif tin_loai == "Tin Lũ":
                    images =   read_ftp_sever_image('tin_TVHV.png')
                    st.image(images,use_column_width=True)
                    # pdf_file = tim_file(read_txt('path_tin/LULU.txt'), '.pdf')
                    # images = export_imaepdf(pdf_file)
                    # for img in images:
                    #     st.image(img)
                
            map_expander = st.expander("Trạm mưa lưu vực")

            with map_expander:
                folium_static(m,width=550)

        with col2:
            with st.expander ("RADA TAM KỲ"):
                # ip = '203.209.181.171'
                # username = 'mpi'
                # password = 'mpi@1234'
                # ssh_directory  = '/home/disk2/KQ_WRF72h/{}/Hinh_00z_36h/Luoi2/MuaL2_11.png'.format(datetime.now().strftime('%d%m%Y'))  # Thay đổi đường dẫn tới tệp ảnh trên máy chủ
                # # image =   read_ftp_sever_image('tin_TVHN.png')
                # image = get_image_from_ssh(ip, username, password, ssh_directory)
                try:
                    image = read_ftp_sever_rada_image()
                    st.image(image, caption='Ảnh RaĐa Tam Kỳ hiện tại', use_column_width=True)
                except:
                    st.error("Không thể lấy ảnh từ máy chủ. Vui lòng kiểm tra lại thông tin.")

            map_windy = st.expander("Windy")
            map_windy._iframe(src='https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=default&metricTemp=default&metricWind=default&zoom=11&overlay=wind&product=ecmwf&level=surface&lat=15.356&lon=108.158&detailLat=15.333856148597976&detailLon=108.18099975585939',height=500)
        #theme
        hide_st_style=""" 

        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """

    #all graphs we use custom css not streamlit 
    theme_plotly = None 
    # load Style css
    # with open('style.css')as f:
    #     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    # logo_image = 'image/logo_ttb.png'
    # authenticator.logout("Logout", "sidebar")
    # st.header("ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ")    
    # tao thanh slidebar va du lieu trong slidebar
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    with st.sidebar:
        st.image("image/logo_ttb.png",width=150)
        # tthc = pd.read_excel('data/Thongso.xlsx',index_col='STT')
        # st.dataframe(tthc)


    def sideBar():
        with st.sidebar:
            selected=option_menu(
                menu_title="Danh Sách",
                options=["Trang chủ","KTTV"],
                icons=["house","eye"],
                menu_icon="cast",
                default_index=0
            )
        if selected=="Trang chủ":
            hochua_quangnam()
        if selected=="KTTV":
            st.warning("Chưa cấp quyền truy cập")

    sideBar()


