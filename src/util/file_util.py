import base64
import os

import streamlit as st


def display_file_content(file_path):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	current_dir = current_dir.replace('src', 'static')
	current_dir = current_dir.replace('util', 'text')
	full_file_path = os.path.join(current_dir, file_path)
	if os.path.exists(full_file_path):
		with open(full_file_path, "r", encoding = "utf-8") as file:
			try:
				lines = file.readlines()
				content = "\n".join(lines).strip()
				return content
			except UnicodeDecodeError:
				st.error(
					f"Tệp tin '{full_file_path}' không thể đọc với encoding utf-8.")
	else:
		st.error(f"Tệp tin '{full_file_path}' không tồn tại.")


def embed_image(file_path, width, height):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	current_dir = current_dir.replace('src', 'static')
	current_dir = current_dir.replace('util', 'images')
	full_file_path = os.path.join(current_dir, file_path)

	with open(full_file_path, "rb") as image_file:
		encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
	html_code = f"""
    <div style="display: flex; justify-content: center;">
        <img src='data:image/jpeg;base64,{encoded_image}' alt='Ten_Hinh_Anh' width='{width}%' height='{height}' style='border-radius: 15pt; margin-bottom:5%;'>
    </div>
    """
	st.markdown(html_code, unsafe_allow_html = True)
