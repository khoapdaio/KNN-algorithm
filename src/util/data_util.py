from sklearn.datasets import load_iris, load_diabetes, load_digits, load_breast_cancer, load_linnerud, load_wine
import streamlit as st

dataset_dict = {"load_diabetes": load_diabetes,
                "load_digits": load_digits,
                "load_iris": load_iris,
                "load_breast_cancer": load_breast_cancer,
                "load_linnerud": load_linnerud,
                "load_wine": load_wine, }


def choose_data():
	option = st.selectbox("Chọn dữ liệu trong thư viện sklearn", ("load_diabetes",
	                                                              "load_digits",
	                                                              "load_iris",
	                                                              "load_breast_cancer",
	                                                              "load_linnerud",
	                                                              "load_wine",))
	return dataset_dict[option]
