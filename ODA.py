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
def download_csv(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
    return href
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
# @st.cache_data
def graphs_h(df_h):
    # print(df_h)
    # Vẽ biểu đồ
    fig = px.line(df_h, x = 'time',y = df_h.columns)
    # fig = px.line(df_h, x = 'Thời gian' ,y=[df_h['Q đến (m3/s)'],df_h['Q điều tiết (m3/s)']],)
    fig.update_traces(mode="lines")
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="orange", spikesnap="cursor", spikemode="across",spikethickness=2)
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout(spikedistance=1000, hoverdistance=100)
    # Cập nhật layout của biểu đồ
    fig.update_layout(
        title="<b>Đường quá trình mực nước</b>",
        xaxis=dict(tickmode="linear",tickformat="%d-%m-%Y %H:%M",dtick="H1",tickangle=-30),
        plot_bgcolor="rgba(1,0,0,0)",
        yaxis=dict(showgrid=True,title="Mực nước (m))"),
        legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
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
def chaymua(name_tinh,bd,kt):
    # Quảng Ngãi
    df = CDH_TTB_API.TTB_API_mua("TS_ID/TTB/" + name_tinh + "_TTB_Mua.txt",bd,kt)
    # # bàn tong ket tong ket mua
    tk = CDH_TTB_API.xulysolieu_mua(df)
    return tk,df

@st.cache_data
def chaymucnuoc(name_tinh,yeuto,bd,kt):
    yt = ['MucNuoc','Gio','Nhiet','Am','Ap']
    ty = ['H','Gio','Nhiet','Am','Ap']
    # Quảng Ngãi
    df = CDH_TTB_API.TTB_API_mucnuoc("TS_ID/TTB/" + name_tinh + "_TTB_{}.txt".format(ty[yt.index(yeuto)]),bd,kt)
    # print(df)
    # # bàn tong ket tong ket mua
    tk = CDH_TTB_API.xulysolieu_h(df)
    return tk,df

# @st.cache_data    
def getdulieu(tinh,yeuto,bd,kt):
    if yeuto =='Mua':
        tk,solieugoc = chaymua(tinh,bd,kt)
    else:
        tk,solieugoc = chaymucnuoc(tinh,yeuto,bd,kt)
    
    return tk,solieugoc

def solieu_kttv():
    # st.set_page_config(layout="wide")
    # st.markdown('<h1 style="font-size:25px;color:Blue;font-family: Times New Roman;text-align: center;">VIEW SỐ LIỆU ODA</h1>', unsafe_allow_html=True)# tạo header màu xanh màu xanh time new roman
    # now = datetime.now()
    with st.sidebar:
        tinh,yeutos = st.columns(2)
        # Tạo một danh sách các tùy chọn cho combobox
        provin = ["QNGA", "QBIN", "QTRI", "THUE", "DNAN", "QNAM"]
        yeuto = ['MucNuoc','Mua','Gio','Nhiet','Am','Ap']
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
            
    tichluy,bieudo = st.columns(2) # tao 2 cot tram va bieu do
    

    # if st.button("View"):

    tk,solieugoc = getdulieu(selected_tinh,selected_yeuto,datetime.combine(ngaybd, gio_batdau),datetime.combine(ngaykt, gio_ketthuc))
    # print(tk)
    
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
        # print(selected_rows['Tram'].to_list())
    with bieudo:
        solieugoc.reset_index(drop=False,inplace=True)
        # print(solieugoc)
        # tramve = selected_rows['Tram'].to_list()
        # print(selected_yeuto)
        if 'Mua' in selected_yeuto:
            st.plotly_chart(graphs_mua(solieugoc[['time']+  selected_rows['Tram'].to_list()]))
        else:
            # print(solieugoc)
            st.plotly_chart(graphs_h(solieugoc[['time']+  selected_rows['Tram'].to_list()]))
    with st.expander("VIEW SỐ LIỆU"):

        showData=st.multiselect('Filter: ',solieugoc.columns,default=solieugoc.columns.tolist())
        st.dataframe(solieugoc[showData],use_container_width=True)
        if st.button('Tải dữ liệu'):
            st.markdown(download_csv(solieugoc[showData]), unsafe_allow_html=True) 

    # print(solieugoc)
    st.markdown('ĐẶC TRƯNG SỐ LIỆU',unsafe_allow_html=True)
    if selected_yeuto == 'Mua':
        tongketsolieu = solieugoc[solieugoc['time'].dt.minute==0].iloc[:,1:].agg(['sum','max'])
        st.dataframe(tongketsolieu)
    elif selected_yeuto == 'MucNuoc':
        tongketsolieu = solieugoc[solieugoc['time'].dt.minute==0].agg(['mean','max', 'min'])
        st.dataframe(tongketsolieu)
    else:    
        tongketsolieu = solieugoc[solieugoc['time'].dt.minute==0].agg(['mean','max', 'min'])
        st.dataframe(tongketsolieu)        