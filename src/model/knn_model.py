from collections import Counter

import numpy as np


class KnnModel():
	# Khởi tạo các biến trong hàm init
	def __init__(self, k = 3, metric = 'euclidean', p = None):
		self._k = k
		self._metric = metric
		self._p = p

	def set_k(self, k):
		self._k = k

	def set_p(self, p):
		self._p = p

	def set_metric(self, metric):
		self._metric = metric

	def get_metric(self):
		return self._metric

	# Xây dựng độ đo euclidenan
	def euclidean(self, v1, v2):
		return np.sqrt(np.sum((v1 - v2) ** 2))

	# Xây dựng độ đo manhattan
	def manhattan(self, v1, v2):
		return np.sum(np.abs(v1 - v2))

	# Xây dựng độ đo minkowski
	def minkowski(self, v1, v2, p = 2):
		return np.sum(np.abs(v1 - v2) ** p) ** (1 / p)

	def chebyshev_distance(self, x1, x2):
		return np.max(np.abs(x1 - x2))

	# Xây dựng hàm fit
	def fit(self, X_train, y_train):
		self.X_train = X_train
		self.y_train = y_train

	# Xây dựng hàm Predict
	def predict(self, X_test):
		preds = []
		for test_row in X_test:
			nearest_neighbours = self.get_neighbours(test_row)
			majority = Counter(nearest_neighbours).most_common(1)[0][0]
			preds.append(majority)
		return np.array(preds)

	# Xây dựng hàm lấy điểm gần nhất
	def get_neighbours(self, test_row):
		distances = self.get_distances(test_row)
		# Xác định k
		neighbours = list()
		for i in range(self._k):
			neighbours.append(distances[i][2])

		return neighbours

	def get_distances(self, test_row):
		distances = list()

		# Tính khoảng cách tất cả các điểm trong tập train
		for (train_row, train_class) in zip(self.X_train, self.y_train):
			if self._metric == 'euclidean':
				dist = self.euclidean(train_row, test_row)
			elif self._metric == 'manhattan':
				dist = self.manhattan(train_row, test_row)
			elif self._metric == 'minkowski':
				dist = self.minkowski(train_row, test_row, self._p)
			else:
				raise NameError('Supported metrics are euclidean, manhattan and minkowski')
			distances.append((dist, train_row,train_class))

		# sắp xếp lại
		distances.sort(key = lambda x: x[0])
		return distances

	def score(self, y_pred, y_test):
		return np.sum(y_pred == y_test) / len(y_test)
