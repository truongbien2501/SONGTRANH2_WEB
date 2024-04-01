import os
import pandas as pd
from  datetime import datetime,timedelta
def read_line(pth):
    with open(pth, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines


def read_txt(pth):
    file = open(pth,'r')
    contents = file.read()
    file.close()
    return contents
    
def tim_file(duong_dan,kieufile):
    # Lấy danh sách tất cả các tệp tin trong thư mục
    tat_ca_files = os.listdir(duong_dan)
    # Lọc các tệp tin có phần mở rộng là ".pdf"
    pdf_files = [file for file in tat_ca_files if file.lower().endswith(kieufile)]
    # Sắp xếp các tệp tin theo thứ tự thời gian sửa đổi giảm dần
    pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(duong_dan, x)), reverse=True)
    # Kiểm tra nếu có ít nhất một file PDF
    if pdf_files:
        duong_dan_cuoi_cung = os.path.join(duong_dan, pdf_files[0])
        return duong_dan_cuoi_cung.replace('~$','')
    else:
        return None

def vitridat():
    df1 = pd.read_excel(tim_file(read_txt('path_tin/DATA_EXCEL.txt'),'.xlsm'),sheet_name='H')
    now = datetime.now()
    now = datetime(int(now.strftime('%Y')),int(now.strftime('%m')),int(now.strftime('%d')),8)
    kt = (now - timedelta(days=1))
    df1.rename(columns={'Ngày':'time','Trà Khúc':'trakhuc','Sông Vệ':'songve','Trà Bồng\n(Châu Ổ)':'chauo','Trà Câu':'tracau'},inplace=True)
    df1=df1[['time','trakhuc','songve','chauo','tracau']]
    # df1['time'] = pd.to_datetime(df1['time'])
    dt_rang = pd.date_range(start=datetime(2022,1,1,1), periods=len(df1['time']), freq="H")
    df1['time'] = dt_rang
    df1 = df1.loc[df1['time'] > kt ]
    return(df1.index[0])