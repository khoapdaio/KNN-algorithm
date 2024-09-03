import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

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

		tab1, tab2 = st.tabs(["1", "2"])

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
			df_statistics = data[list_statistics + ['target']]
			knn_model.fit(data[list_statistics].values, y)

			x_point = st.number_input("X value", value = 1.0)
			y_point = st.number_input("Y value", value = 1.0)

			if st.button('Predict with point'):
				x_1 = df_statistics[df_statistics['target'] == 0][list_statistics[0]]
				x_2 = df_statistics[df_statistics['target'] == 1][list_statistics[0]]
				x_3 = df_statistics[df_statistics['target'] == 2][list_statistics[0]]
				y_1 = df_statistics[df_statistics['target'] == 0][list_statistics[1]]
				y_2 = df_statistics[df_statistics['target'] == 1][list_statistics[1]]
				y_3 = df_statistics[df_statistics['target'] == 2][list_statistics[1]]

				fig = go.Figure()

				# Add traces
				fig.add_trace(go.Scatter(x = x_1, y = y_1,
				                         mode = 'markers',
				                         name = data_set().target_names[0], ))
				fig.add_trace(go.Scatter(x = x_2, y = y_2,
				                         mode = 'markers',
				                         name = data_set().target_names[1]))
				fig.add_trace(go.Scatter(x = x_3, y = y_3,
				                         mode = 'markers',
				                         name = data_set().target_names[2]))

				distances = knn_model.get_distances([x_point, y_point])
				x_4 = []
				y_4 = []
				for i in range(k_value):
					x_4.append(distances[i][1][0])
					x_4.append(x_point)
					y_4.append(distances[i][1][1])
					y_4.append(y_point)
				fig.add_trace(go.Line(x = x_4, y = y_4, name = "distance",text = list_statistics[0]))
				st.plotly_chart(fig)
			X = df_statistics.values
			y = data['target'].values

			knn_model.fit(X, y)

	def __get_formula(self, name):
		return self.formula_dic[name]()
