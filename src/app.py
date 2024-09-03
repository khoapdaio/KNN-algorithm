import streamlit as st
from streamlit_option_menu import option_menu

from util import choose_data
from view import IntroductionView, StaticView, ModelView, ContactView


view_dict = {
	"Overview": IntroductionView,
	"Statistics": StaticView,
	"Model": ModelView,
	"Contact": ContactView,
}

def select_view(selected_option):
	return view_dict[selected_option]()


def main():
	st.set_page_config(layout = "wide")

	select_dataset = choose_data()


	st.sidebar.markdown("""
	        <h1 style='font-size:35px;text-align:center'>Khoapd</h1>
	    """, unsafe_allow_html = True)

	st.sidebar.markdown("""
	        <div style="display: flex; justify-content: center;margin-bottom:0">
	            <img src='/static/images/avatar.png' alt='Ten_Hinh_Anh' width='60%' style='border-radius:50%;margin-bottom:12%;'>
	        </div>
	        """, unsafe_allow_html = True)
	st.sidebar.info('❤🌤️Welcome to project🌤️❤️')
	st.sidebar.markdown("---")


	with st.sidebar:
		selected_option = option_menu(
			menu_title = "Main Menu",
			options = ["Overview", "Statistics", "Model", "Contact"],
			icons = ["house", "book", "modem", "phone"],
			menu_icon = "menu-up"

		)
	selected_view = select_view(selected_option)
	selected_view.display(select_dataset)

	st.sidebar.markdown("---")
	st.sidebar.info("Created and designed by [Pham Dang Khoa](https://github.com/khoapdaio)")


if __name__ == '__main__':
	main()
