import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
import base64
import pandas as pd
import mpld3
# Thiết lập kích thước và chế độ hiển thị trang ứng dụng
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Streamlit Demo", page_icon=":guardsman:")
# st.title("ĐÀI KHÍ TƯỢNG THỦY VĂN TỈNH QUẢNG NGÃI") # tạo tiêu đề
st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">ĐÀI KHÍ TƯỢNG THỦY VĂN TỈNH QUẢNG NGÃI</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman


df = pd.read_excel("data.xlsm",sheet_name='H')
st.dataframe(df)

# Tạo nút để xuất dữ liệu bảng
if st.button('Load DATA'):
    st.warning('Đây là thông báo cảnh báo!')

if st.button('Export data'):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)


# with st.beta_container():
#     st.write("This is in the container")

# Vẽ biểu đồ và hiển thị trong ứng dụng
fig, ax = plt.subplots()
ax.plot(df['Ngày'], df['Sông Vệ'])
ax.set(title='BIỂU ĐỒ',xlabel = 'Thời Gian',ylabel= 'Mực nước',anchor='C')
plt.xticks(rotation=45, size=6)


# # Hiển thị biểu đồ trên Streamlit
st.pyplot(fig)



# Tạo bản đồ Quảng Ngãi tương tự như bước 2
lat = 15.12047
log = 108.79232
m = folium.Map(location=[lat, log], zoom_start=9)
folium.Marker([lat, log], popup='Trà Khúc').add_to(m)

# Hiển thị bản đồ trong ứng dụng Streamlit
st.write("Vị trí dự báo")
folium_static(m)


