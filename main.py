import streamlit as st
from pages import Page
from mock_up import show_data_model
from system_dependencies import show_system_dependencies

def main():
    st.set_page_config(page_title="System Management Tools", layout="wide")

    # Password protection
    if check_password():
        # Create navigation
        pages = {
            "Data Model": Page("⚙️ Data Model: System Management", show_data_model),
            "System Dependencies": Page("🔄 System Dependencies", show_system_dependencies)
        }

        # Sidebar navigation
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(pages.keys()))

        # Run the selected page
        pages[selection].run()

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Showmethemoney":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("⚠️ Password incorrect")
        return False
    else:
        return True

if __name__ == "__main__":
    main()
