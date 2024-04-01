import streamlit as st
import paramiko
import io
from PIL import Image
import io
import PIL
from ftplib import FTP

def get_image_from_ssh(ip, username, password, ssh_path):
    # Tạo một kết nối SSH đến máy chủ
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(ip, username=username, password=password)
        # Lấy nội dung của tệp ảnh từ máy chủ
        sftp_client = ssh_client.open_sftp()
        image_file = sftp_client.open(ssh_path, 'rb')
        image_data = image_file.read()
        sftp_client.close()
        ssh_client.close()
        
        # Chuyển dữ liệu ảnh thành đối tượng hình ảnh (PIL)
        image = Image.open(io.BytesIO(image_data))
        return image
    except paramiko.AuthenticationException:
        st.error("Lỗi xác thực SSH. Vui lòng kiểm tra lại tên người dùng và mật khẩu.")
    except paramiko.SSHException:
        st.error("Lỗi khi kết nối đến máy chủ qua SSH.")
    except FileNotFoundError:
        st.error("Không tìm thấy tệp ảnh trên máy chủ.")
    except Exception as e:
        st.error(f"Lỗi không xác định: {e}")
        
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