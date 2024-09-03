import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp


class DescriptiveStatics:
	def __init__(self, df, list_statistics):
		self.df = df
		self.df_statistic = self.df[list_statistics]

	def describe(self):
		describe = self.df.describe()
		return describe

	def subplot_histograms(self):
		row = int(self.df_statistic.shape[1] // 4 + 1)
		fig = sp.make_subplots(rows = row, cols = 4, subplot_titles = self.df_statistic.columns[0:])

		for i, feature in enumerate(self.df_statistic.columns[0:]):
			fig.add_trace(go.Histogram(x = self.df_statistic[feature]), row = (i // 4) + 1, col = (i % 4) + 1)
		fig.update_layout(title_text = 'Histogram Subplots', showlegend = False,
		                  width = 13 * 80,
		                  height = 10 * (row * 40),
		                  title_x = 0.4,
		                  bargap = 0.04)
		return fig

	def pairplot(self):
		fig = px.scatter_matrix(self.df_statistic,
		                        dimensions = [i for i in self.df_statistic.columns if i is not "target"],
		                        color = None if self.df_statistic.empty else "target")
		fig.update_layout(title_text = 'Mối quan hệ giữa các biến',
		                  width = 13 * 80,
		                  height = 12 * 80,
		                  title_x = 0.4, )
		return fig

	def heatmap(self):
		data_heatmap = self.df_statistic.columns.difference(["target"])
		correlation_matrix = self.df_statistic[data_heatmap].corr()

		fig = px.imshow(
			correlation_matrix,
			x = data_heatmap,
			y = data_heatmap,
			color_continuous_scale = 'RdYlGn',
			labels = dict(color = 'Correlation'),
			title = 'Heatmap'
		)

		fig.update_layout(xaxis = dict(tickangle = -45),
		                  yaxis = dict(tickangle = 0),
		                  width = 13 * 80,
		                  height = 12 * 80,
		                  title_x = 0.4, )
		return fig
