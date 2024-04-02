import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
# from docx import Document
# from docx2txt import process
from func.load_image import get_image_from_ssh,read_ftp_sever_image
from func.CDH_TTB_API import H_hochua,dungtich_hochua
from func.bieudo import ve_H_hochua,ve_Q_veho,Bieudo_Q_H,Mucnuoc_songtranh,vebieudomua
from func.pdf_image import export_imaepdf
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader
from func.Seach_file import tim_file,read_txt
from datetime import datetime,timedelta

# Thiết lập kích thước và chế độ hiển thị trang ứng dụng
# st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="KTTV TTB", page_icon="	:sun_behind_rain_cloud:")
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Hồ chứa KTTV TTB", page_icon="	:sun_behind_rain_cloud:")
with open("CSS/styles.css",'r',encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# tao form dang nhap
with open(r'D:\PM_PYTHON\APP_WEB\login\list_uer.yaml') as file:
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
    logo_image = 'image/logo_ttb.png'
    authenticator.logout("Logout", "sidebar")
    # Hiển thị tiêu đề tùy chỉnh
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
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown('<h1>ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ</h1>', unsafe_allow_html=True)
    # st.markdown(f'<img class="logo" src="{logo_image}">', unsafe_allow_html=True)
    # st.markdown(f'<img class="banner" src="{banner_image}">', unsafe_allow_html=True)
    # st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
    # st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">ĐÀI KHÍ TƯỢNG THUỶ VĂN TỈNH QUẢNG NGÃI</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
    st.write('----------------------------')
    

    # load muc nuoc
    h_songtranh2 = Mucnuoc_songtranh()
    array_data = np.genfromtxt('TS_ID/H_W.txt', delimiter=",",names=True,encoding=None)
    row_index = np.where(array_data['H']==float(h_songtranh2))
    dungtich_songtranh2 = str(array_data['W'][row_index])[1:-1]

    # tinh dung tich cac ho chua
    data = {"Hồ": ["Sông Tranh", "A Vương", "Sông Bung"],
            "Mực nước(m)": ['{:.1f}'.format(h_songtranh2), '-', '-'],
            "Dung tích (tr/m3)": [dungtich_songtranh2, "-", "-"],
            "Tỷ lệ(%)": ['-', '-', "-"],
            "MNDBT": ['-', '-', '-'],
            "MN_CHẾT": ['-', '-', '-']
            }

    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame(data)
    custom_css = """
    <style>
        table {
            background-color: RGBA(255, 100, 50, 0.5);
            margin: auto; /* Để căn giữa bảng theo chiều ngang */
            margin-right: auto;
        }
        table th {
            font-size: 20px;
            color: black;
            font-weight: bold;
            text-align: center;
        }
        table td {
            color: black;
            font-weight: bold;
            text-align: center;
        }
    </style>
    """
    st.markdown(custom_css,unsafe_allow_html=True)
    # Tạo bảng
    st.table(df)


    # Tạo hộp văn bản và lấy giá trị người dùng nhập vào
    # Tạo bố cục gồm 2 cột
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
    # Nhúng mã CSS tùy chỉnh vào ứng dụng
    st.markdown(custom_css, unsafe_allow_html=True)
    # Trong cột thứ hai, tạo lịch để chọn ngày kết thúc
    ngaykt = kt.date_input("Ngày kết thúc",value=datetime(datetime.now().year,datetime.now().month,datetime.now().day,datetime.now().hour))
    gio_ketthuc = kt_gio.time_input('Giờ kết thúc',value=datetime.strptime(datetime.now().strftime("%H:00"),"%H:00"))
 
 
    map_h,map_q,data_mua,solieu_hq = Bieudo_Q_H(datetime.combine(ngaybd, gio_batdau),datetime.combine(ngaykt, gio_ketthuc))

    # hien thị bảng số liệu H Q
    custom_css = """
    <style>
        table {
            background-color: RGBA(255, 255, 255, 0.5);
            margin: auto; /* Để căn giữa bảng theo chiều ngang */
            margin-right: auto;
        }
        table th {
            font-size: 20px;
            color: black;
            font-weight: bold;
            text-align: center;
        }
        table td {
            color: black;
            font-weight: bold;
            text-align: center;
        }
    </style>
    """
    st.markdown(custom_css,unsafe_allow_html=True)
    # solieu_hq = solieu_hq.sort_values(by='Thời gian',ascending=False)
    # st.table(solieu_hq)
    
    
    st.pyplot(map_h)
    # Nhúng mã CSS để tùy chỉnh biểu đồ
    custom_css = """
    <style>
        /* Thêm CSS tùy chỉnh cho biểu đồ */
        .stImage {
            border: 2px solid red;
            border-radius: 10px;
            background-color: rgba(255, 0, 0);
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.pyplot(map_q)
    # print(data_mua)
    # name_eng = ['TRABUI', 'tracang', 'tradon', 'tragiac', 'traleng', 'tralinh','TRAMAI', 'UBNDHnamTM', 'tramdapst2', 'tranam2', 'travan']
    chontrammua = st.selectbox("Chọn trạm", ['Trà Bùi', 'Trà Căng', 'Trà Dơn', 'Trà Giác', 'Trà Leng', 'Trà Linh','Trà Mai', 'UBNDHnamTM', 'Trà Đốc(Đập chính)', 'Trà Nam', 'Trà Vân'])
    tramve = data_mua[['time',chontrammua]]
    # print(tramve)
    images =  vebieudomua(tramve)
    st.pyplot(images)
 
    
    print(data_mua)

    # tao thanh slidebar va du lieu trong slidebar
    # with st.sidebar:
    #     st.sidebar.markdown('''
    #         <h1 style="text-align: center;">Thông số hồ chứa</h1>
    #     ''', unsafe_allow_html=True)
        
    # Danh sách các điểm
    tram_kttv = {'Câu Lâu\n' + 'Mực nước:96cm': (15.857806467135058, 108.27289741859273),
                 'Giao Thủy\n' + 'Mực nước:{}cm'.format(-0.25): (15.846, 108.109),
                 'Nông Sơn\n' + 'Mực nước:2919cm':(15.70276202116165, 108.03392429139377),
                'Trà Đốc\n' + 'Lượng mưa 1h:0mm': (15.331688, 108.147511),
                'Trà Bui\n' + 'Lượng mưa 1h:0mm': (15.34661, 108.041526),
                'Trà Giác\n' + 'Lượng mưa 1h:0mm': (15.240458, 108.178398),
                'Trà Dơn\n' + 'Lượng mưa 1h:0mm': (15.243961, 108.0858880),
                'Trà Leng\n' + 'Lượng mưa 1h:0mm': (15.272192, 108.014046),
                'Trà Mai(UBND)\n' + 'Lượng mưa 1h:0mm': (15.1547, 108.1085),
                'Trà Cang\n' + 'Lượng mưa 1h:0mm': (15.1046490, 108.0714240),
                'Trà Vân\n' + 'Lượng mưa 1h:0mm': (15.1130910, 108.1800410),
                'Trà Nam 2\n' + 'Lượng mưa 1h:0mm': (14.9871600, 108.1336140),
                'Trà Linh\n' + 'Lượng mưa 1h:0mm': (15.030926, 108.0241060),              
                'Quần đảo Hoàng Sa(Việt Nam)': (16.6,112.7),
                'Quần đảo Trường Sa(Việt Nam)': (9.45,112.904)
                }
    # Tạo bản đồ Quảng Ngãi
    m = folium.Map(location=[15.3371600,108.39232], 
                zoom_start=9,
                    width='95%',  # Định dạng kích thước chiều rộng
                    height='100%'  # Định dạng kích thước chiều cao
                )
    # Tạo các điểm Marker với Tooltip và thay đổi màu sắc
    for location, coord in tram_kttv.items():
        # print(location)
        # folium.Marker(coord, popup=location, tooltip=location).add_to(m)
        if 'Câu Lâu' in location or 'Giao Thủy' in location or 'Nông Sơn' in location: # bieu tuong thuy chi cho tram do thuy van
            custom_icon = folium.CustomIcon(icon_image="image/thuychi.png", icon_size=(10, 50))
            folium.Marker(coord, popup=location,icon=custom_icon).add_to(m)
            # folium.Marker(coord, popup=location,icon=folium.Icon(color='blue')).add_to(m)
        else:
            custom_icon = folium.CustomIcon(icon_image="image/mua.jpg", icon_size=(30, 30)) # bieu tuong mua cho tram do mua
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
                st.image(images)
            elif tin_loai == "Hạn vừa":
                images =   read_ftp_sever_image('tin_TVHV.png')
                st.image(images)
            elif tin_loai == "Tin Lũ":
                images =   read_ftp_sever_image('tin_TVHV.png')
                st.image(images)
                # pdf_file = tim_file(read_txt('path_tin/LULU.txt'), '.pdf')
                # images = export_imaepdf(pdf_file)
                # for img in images:
                #     st.image(img)
            
        map_expander = st.expander("Trạm mưa lưu vực")
        with map_expander:
            folium_static(m)
            
    with col2:
        with st.expander ("Kết quả Mô Hình Số"):
            ip = '203.209.181.171'
            username = 'mpi'
            password = 'mpi@1234'
            ssh_directory  = '/home/disk2/KQ_WRF72h/01042024/Hinh_00z_36h/Luoi2/MuaL2_11.png'  # Thay đổi đường dẫn tới tệp ảnh trên máy chủ
            # image =   read_ftp_sever_image('tin_TVHN.png')
            image = get_image_from_ssh(ip, username, password, ssh_directory)
            if image:
                # Hiển thị ảnh bằng cách sử dụng hàm 'image' của Streamlit
                st.image(image, caption='Mưa dự báo', use_column_width=True)
            else:
                st.error("Không thể lấy ảnh từ máy chủ. Vui lòng kiểm tra lại thông tin SSH.")
        map_windy = st.expander("Windy")      
        with map_windy :
            st.markdown('<iframe width="550" height="500" src="https://embed.windy.com/embed2.html?lat=11.265&lon=108.809&detailLat=15.111&detailLon=108.794&width=650&height=450&zoom=5&level=surface&overlay=wind&product=ecmwf&menu=&message=true&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=m%2Fs&metricTemp=%C2%B0C&radarRange=-1" frameborder="0"></iframe>', unsafe_allow_html=True)