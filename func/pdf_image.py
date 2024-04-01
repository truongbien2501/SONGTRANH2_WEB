from func.Seach_file import tim_file,read_txt
from pdf2image import convert_from_path
import os

def export_imaepdf(pdf_file):
    # Thư mục đầu ra cho các hình ảnh
    output_image_folder = "image"

    # Tạo thư mục đầu ra nếu nó không tồn tại
    os.makedirs(output_image_folder, exist_ok=True)

    # Chuyển đổi PDF thành hình ảnh
    images = convert_from_path(pdf_file,500,poppler_path=r'D:\PM_PYTHON\APP_WEB\poppler-23.08.0\Library\bin')
    return images