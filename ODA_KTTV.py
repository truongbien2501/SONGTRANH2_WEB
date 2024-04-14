import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
import base64
import pandas as pd
from datetime import datetime
# from func.load_image import get_image_from_ssh
# from func.CDH_TTB_API import H_hochua
# from func.bieudo import ve_H_hochua,ve_Q_veho
import CDH_TTB_API



# Function to apply conditional formatting
def highlight_greater(val):
    if val >= 50:
        return f'background-color: purple; color: white;'
    elif val >= 30:
        return f'background-color: red; color: white;'
    return ''


# Thiết lập kích thước và chế độ hiển thị trang ứng dụng
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Đài KTTV TTB", page_icon="	:sun_behind_rain_cloud:")
# st.title("ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ\nĐÀI KHÍ TƯỢNG THỦY VĂN TỈNH QUẢNG NGÃI") # tạo tiêu đề
# st.image('image/logo_ttb.png',width=50)
st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">VIEW SỐ LIỆU ĐÀI KHÍ TƯỢNG THUỶ VĂN KHU VỰC TRUNG TRUNG BỘ</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
# st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">ĐÀI KHÍ TƯỢNG THUỶ VĂN TỈNH QUẢNG NGÃI</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
now = datetime.now()


def chaymua(name_tinh):
    # Quảng Bình
    df = CDH_TTB_API.TTB_API_mua("TS_ID/MUA/" + name_tinh + "_TTB_Mua.txt")
    df_sorted = df.sort_index(ascending=False)

    # st.header('Filter Options mưa')
    # min_value = st.slider('Minimum Value', min_value=0, max_value=100, value=0)
    # filtered_df = df_sorted[df_sorted > min_value]

    # Apply ham loc du lieu voi so lieu lon hon 30mm
    df_sorted = df_sorted.style.applymap(highlight_greater).format("{0:.1f}")
    # Sử dụng Streamlit để hiển thị DataFrame
    text_with_background = "<span style='background-color: #ffff00; padding: 5px;font-size: 25px; font-weight: bold;'>Lượng mưa giờ</span>"
    st.markdown(text_with_background, unsafe_allow_html=True)
    # st.write(df_sorted)

    # Sử dụng CSS để tùy chỉnh DataFrame
    st.write(
        df_sorted,
        unsafe_allow_html=True,
        key="custom_dataframe",
    )

    # Đặt mã CSS bên ngoài để tùy chỉnh DataFrame
    st.markdown(
        """
        <style>
        #custom_dataframe {
            background-color: RGBA(255,255, 255, 0.5);
        }
        #custom_dataframe th {
            font-size: 50px;
            font-weight: bold;
        }
        #custom_dataframe td {
            color: black;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # bàn tong ket tong ket mua
    text_with_background = "<span style='background-color: #ffff00; padding: 5px;font-size: 25px; font-weight: bold;'>" + "Tổng kết đến {}".format(now.strftime('%d/%m/%Y %H:00'))+ "</span>"
    st.markdown(text_with_background, unsafe_allow_html=True)
    tk = CDH_TTB_API.xulysolieu_mua(df)
    st.markdown( 
                """
        <style>
        table {
            background-color: RGBA( 240, 255, 255, 1 );
        }
        table th {
            font-size: 15px; /* Đặt cỡ chữ cho các tiêu đề cột */
            font-weight: bold; /* In đậm cho các tiêu đề cột */
        }
        table td {
            color: black;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
    # Hiển thị bảng
    st.table(tk)


# Tạo một danh sách các tùy chọn cho combobox
options = ["QNGA", "QBIN", "QTRI", "THUE", "DNAN", "QNAM"]
# Sử dụng st.selectbox để tạo combobox
selected_option = st.selectbox("Chọn một tùy chọn:", options)

if st.button("View"):
    chaymua(selected_option)
# else:
#     st.write("Hãy nhấn vào nút.")

# login_button = st.button("View", key="login_button")
