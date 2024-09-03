import pandas as pd
import streamlit as st

from model import DescriptiveStatics
from view import BaseView


class StaticView(BaseView):
	def display(self, data_set):
		st.header("Thống kê mô tả")

		data = pd.DataFrame(data_set().data, columns = data_set().feature_names)
		data['target'] = data_set().target

		df_statistic = st.multiselect("Chọn cột để thống kê", data.columns)

		descriptive = DescriptiveStatics(data, df_statistic)
		st.dataframe(descriptive.describe(), width = 13 * 80)
		st.subheader('Histogram')
		st.plotly_chart(descriptive.subplot_histograms())
		st.subheader("Pairplot")
		st.plotly_chart(descriptive.pairplot())
		st.subheader("Heatmap")
		st.plotly_chart(descriptive.heatmap())
