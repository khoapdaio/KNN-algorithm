import pandas as pd
import streamlit as st

from util import display_file_content, embed_image, choose_data
from view import BaseView




class IntroductionView(BaseView):

	def display(self,data_set):
		st.title("K-Nearest Neighbors")
		data = pd.DataFrame(data_set().data, columns = data_set().feature_names)

		total_rows = data.shape[0]
		total_columns = data.shape[1]
		dimension_data = data.shape
		col1, col2, col3 = st.columns(3)

		with col1:
			st.info(f"**Total Rows:**\n\n{total_rows} rows")
		with col2:
			st.success(f"**Total Columns:**\n\n{total_columns} columns")

		with col3:
			st.warning(f"**Dimension:**\n\n{dimension_data} ")
		st.subheader("Overview")
		st.dataframe(data.head(), width = 13 * 80)
		file_path = "../../static/images/knn_overview.png"
		embed_image(file_path = file_path, width = 60, height = 'auto')
		st.header("Về thuật toán")
		st.info(display_file_content('../../static/text/KNN_kn.txt'))
		col4, col5 = st.columns(2)
		with col4:
			st.subheader("Nguyên lý hoạt động cơ bản")
			st.info(display_file_content('../../static/text/KNN_nlhdcb.txt'))

		with col5:
			st.subheader("Bài toán giải quyết")
			st.info(display_file_content('../../static/text/KNN_vdgq.txt'))
		st.subheader("Giải thích nguyên lý")
		st.info(display_file_content('../../static/text/KNN_nlhdct.txt'))
		embed_image('../../static/images/nguyenlihoatdong_knn.png', width = 40, height = 'auto')
