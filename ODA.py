import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import folium
import base64
import pandas as pd
from datetime import datetime,timedelta
import time
from func import CDH_TTB_API
import plotly.express as px
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
    fig_mua.layout.xaxis.fixedrange = True
    fig_mua.layout.yaxis.fixedrange = True
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
       title="<b>Đường quá trình mực nước</b>",
       color_discrete_sequence=["#0083b8"],
       template="plotly_white",
    )
    fig_mucnuoc.update_traces(mode="lines")
    fig_mucnuoc.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig_mucnuoc.update_yaxes(showspikes=True, spikecolor="orange", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig_mucnuoc.layout.xaxis.fixedrange = True
    fig_mucnuoc.layout.yaxis.fixedrange = True
    fig_mucnuoc.update_layout(spikedistance=1000, hoverdistance=100)
    # fig_mucnuoc.update_layout(
    # xaxis=dict(tickmode="linear"),
    # plot_bgcolor="rgba(0,0,0,0)",
    # yaxis=(dict(showgrid=True))
    #  )
    return fig_mucnuoc
# Function to apply conditional formatting
def highlight_greater(val):
    if val >= 50:
        return f'background-color: purple; color: white;'
    elif val >= 30:
        return f'background-color: red; color: white;'
    return ''

def dataframe_with_selections(df):

    df_with_selections = df.copy()
    df_with_selections.insert(0, "Chọn", False)
    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Chọn": st.column_config.CheckboxColumn(help="Chọn trạm",required=True),
                       },
        disabled=df.columns,
    )
    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df['Chọn']]
    return selected_rows.drop('Chọn', axis=1)

@st.cache_data
def chaymua(name_tinh):
    # Quảng Ngãi
    df = CDH_TTB_API.TTB_API_mua("TS_ID/TTB/" + name_tinh + "_TTB_Mua.txt")
    # # bàn tong ket tong ket mua
    tk = CDH_TTB_API.xulysolieu_mua(df)
    return tk,df
    
    # print(tk.columns)
    # print(tk.reset_index(drop=False))
    # tk.to_excel('quangngai.xlsx')
    # tk = pd.DataFrame(tk)
    # print(tk.columns)
    # tk = pd.read_excel('quangngai.xlsx')
    # tk.insert(0,'Chọn',False)
    # # st.dataframe(tk)
    # # Hiển thị bảng
    # edited_df  = st.data_editor(tk,column_config={"Chọn": st.column_config.CheckboxColumn("Chọn",help="Chọn trạm",default=True,)},disabled=["widgets"],hide_index=True)
    # # Lấy danh sách các chỉ mục hàng đã chọn
    
    # selected_rows = edited_df[edited_df.Select]
    # print(selected_rows)
    # checked_rows = tk[tk['Chọn']==True]
    # st.write(checked_rows)
    # print(checked_rows)

    # # Lấy DataFrame của các hàng đã chọn
    # selected_df = tk.loc[checked_rows].  

    # selection = dataframe_with_selections(tk)
    # print(selection['Tram'].to_list())
    # st.write("Your selection:")
    # st.write(selection)

def solieu_kttv():
    st.set_page_config(layout="wide")
    st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">VIEW SỐ LIỆU ODA</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
    now = datetime.now()
    with st.sidebar:
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


        st.image("image/logo_ttb.png",width=150)
        tinh,yeutos = st.columns(2)
        # Tạo một danh sách các tùy chọn cho combobox
        provin = ["QNGA", "QBIN", "QTRI", "THUE", "DNAN", "QNAM"]
        yeuto = ['Mua','MucNuoc','Gio','Nhiet','Am','Ap']
        # Sử dụng st.selectbox để tạo combobox
        with tinh:
            selected_tinh = st.selectbox("Chọn tỉnh:", provin)
        with yeutos:
            selected_yeuto = st.selectbox("Chọn yếu tố:", yeuto)
        bd,bd_gio = st.columns(2)
        ngaybd = bd.date_input("Ngày bắt đầu",value=datetime((datetime.now() - timedelta(days=5)).year,(datetime.now() - timedelta(days=5)).month,(datetime.now() - timedelta(days=5)).day))
        gio_batdau = bd_gio.time_input('Giờ bắt đầu',value=datetime.strptime("23:00", "%H:%M"))
        
        kt,kt_gio = st.columns(2)
        # Trong cột thứ hai, tạo lịch để chọn ngày kết thúc
        ngaykt = kt.date_input("Ngày kết thúc",value=datetime(datetime.now().year,datetime.now().month,datetime.now().day,datetime.now().hour))
        gio_ketthuc = kt_gio.time_input('Giờ kết thúc',value=datetime.strptime(datetime.now().strftime("%H:00"),"%H:00"))
            
            
    # if st.button("View"):
    tk,solieugoc = chaymua(selected_tinh)
    tichluy,bando = st.columns(2)
    with tichluy:
        
        df_with_selections = tk.copy()
        df_with_selections.insert(0, "Chọn", False)
        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Chọn": st.column_config.CheckboxColumn(help="Chọn trạm",required=True),
                        },
            disabled=tk.columns,
        )
        # Filter the dataframe using the temporary column, then drop the column
        selected_rows = edited_df[edited_df['Chọn']]
        print(selected_rows['Tram'].to_list())
    with bando:
        solieugoc.reset_index(drop=False,inplace=True)
        # print(solieugoc)
        # tramve = selected_rows['Tram'].to_list()
        print(selected_yeuto)
        if 'Mua' in selected_yeuto:
            st.plotly_chart(graphs_mua(solieugoc[['time']+  selected_rows['Tram'].to_list()]))
        elif 'Mucnuoc'in selected_yeuto:
            st.plotly_chart(graphs_h(solieugoc[['time']+  selected_rows['Tram'].to_list()]))

    # rada,bando1 = st.columns(2)
    # with rada:
    #     # Địa chỉ web bạn muốn nhúng
    #     website_url = "http://hymetnet.gov.vn/radar/TKY"
    #     # Sử dụng thành phần HTML để nhúng trang web
    #     # "<iframe src="{}" style='border:0; width:100%; height:400px;'></iframe>"
        
    # st.components.v1.html(f'<iframe src="http://hymetnet.gov.vn/radar/TKY" width:100%; height:100%></iframe>', scrolling=True)        

solieu_kttv()