import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pkg_resources import require

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from model import KnnModel
from model.plot_knn_model import PlotKnnModel
from util import embed_image
from view import BaseView


def get_euclidean_formula():
	return st.latex(r'''
		d(A,B) = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}
	''')


def get_manhattan_formula():
	return st.latex(r'''
		d(A,B) = |x_1-x_2| + |y_1-y_2|
	''')


def get_minkowski_formula():
	return st.latex(r'''
		d(A,B) = max[(x_1-x_2), (y_1-y_2)]
	''')


class ModelView(BaseView):
	formula_dic = {'euclidean': get_euclidean_formula,
	               'manhattan': get_manhattan_formula,
	               'minkowski': get_minkowski_formula}

	def display(self, data_set):
		col1, col2 = st.columns([1, 1])
		knn_model = KnnModel()
		with col1:
			distance_compute = st.selectbox('Chọn độ đo', self.formula_dic.keys())
			knn_model.set_metric(distance_compute)
			k_value = st.number_input('Chọn giá trị K', value = 5, min_value = 0)
			if distance_compute == 'minkowski':
				p_value = st.number_input("Chọn giá trị P", value = 2.0, min_value = 0.0)
				knn_model.set_p(p_value)
			knn_model.set_k(k_value)
		with col2:
			self.__get_formula(distance_compute)
			embed_image("distance_a_b.png", 40, 'auto')

		X = data_set().data
		y = data_set().target

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 4)
		plot_knn_model = PlotKnnModel()

		tab1, tab2 = st.tabs(["Dự đoán", "Dự đoán theo điểm"])

		with tab1:
			if st.button('Predict'):
				knn_model.fit(X_train, y_train)
				y_pred = knn_model.predict(X_test)

				accuracy = knn_model.score(y_pred, y_test)
				st.success(f"Độ chính xác: {accuracy}%")

				st.plotly_chart(plot_knn_model.plot_confusion_matrix(y_test, y_pred))

				report = classification_report(y_test, y_pred, output_dict = True)
				st.table(pd.DataFrame(report))

		with tab2:
			data = pd.DataFrame(data_set().data, columns = data_set().feature_names)
			data['target'] = data_set().target

			list_statistics = st.multiselect("Chọn cột để thống kê", data.columns, max_selections = 2)
			knn_model.fit(data[list_statistics].values, y)

			x_point = st.number_input("X value", value = 1.0)
			y_point = st.number_input("Y value", value = 1.0)

			if st.button('Predict with point'):
				distances = pd.DataFrame(knn_model.get_distances([x_point, y_point]),
				                         columns = ['Distance', 'Neighbor Point', 'N.Class'])
				st.dataframe(distances, width = 320)


	def __get_formula(self, name):
		return self.formula_dic[name]()
