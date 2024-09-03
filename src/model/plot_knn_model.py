import plotly.graph_objects as go
from sklearn import metrics


class PlotKnnModel:

	def plot_distance_from_point(self, point, X, y):
		pass

	def plot_confusion_matrix(self, y_test, y_pred):
		cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

		fig = go.Figure()
		cell_values = [[cnf_matrix[1, 1], cnf_matrix[0, 1]],
		               [cnf_matrix[1, 0], cnf_matrix[0, 0]]]
		fig.add_trace(go.Heatmap(z = cell_values,
		                         x = ['Predicted Positive', 'Predicted Negative'],
		                         y = ['Actual Positive', 'Actual Negative'],
		                         colorscale = "YlGnBu",
		                         showscale = True,
		                         colorbar = dict(tickvals = [val for sublist in cell_values for val in sublist],
		                                         ticktext = [str(val) for sublist in cell_values for val in sublist])))
		fig.update_layout(title = 'Confusion Matrix',
		                  xaxis = dict(title = 'Predicted label'),
		                  yaxis = dict(title = 'Actual label'),
		                  width = 13 * 80,
		                  height = 8 * 80,
		                  title_x = 0.45)

		return fig
