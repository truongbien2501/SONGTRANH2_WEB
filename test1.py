import pandas as pd
from ftplib import FTP

# Thông tin kết nối FTP
ftp_host = '203.209.181.174'
ftp_user = 'admin'
ftp_password = 'Supportdng'
ftp_directory = '/DAKDRINH/DATA'
excel_file_name = 'DR_THUYVAN.xlsx'

# Kết nối đến máy chủ FTP
ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_password)

# Di chuyển đến thư mục chứa tệp Excel
ftp.cwd(ftp_directory)

# Tạo một tệp trống để lưu dữ liệu từ FTP
local_excel_file = 'local_excel_file.xlsx'
# Tải tệp Excel từ FTP về máy cục bộ
with open(local_excel_file, 'wb') as local_file:
    ftp.retrbinary('RETR ' + excel_file_name, local_file.write)
# Đọc tệp Excel bằng pandas
df = pd.read_excel(local_excel_file)
# Bây giờ bạn có thể sử dụng DataFrame df cho các xử lý dữ liệu
# Đóng kết nối FTP
ftp.quit()
print(df)
# # Xoá tệp Excel cục bộ nếu bạn không cần nó nữa
# import os
# os.remove(local_excel_file)