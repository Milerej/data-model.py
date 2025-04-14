import streamlit as st
from pages import Page
from mock_up import show_data_model
from system_dependencies import show_system_dependencies

def main():
    st.set_page_config(
        page_title="System Management Tools", 
        layout="wide",
        initial_sidebar_state="expanded"  # This ensures the sidebar is visible
    )

    # Add custom CSS to ensure sidebar visibility
    st.markdown("""
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 300px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 300px;
            margin-left: -300px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Password protection
    if check_password():
        # Create navigation
        pages = {
            "Data Model": Page("⚙️ Data Model: System Management", show_data_model),
            "System Dependencies": Page("🔄 System Dependencies", show_system_dependencies)
        }

        # Sidebar navigation with some styling
        with st.sidebar:
            st.title("Navigation")
            st.markdown("""
                <style>
                    .sidebar .sidebar-content {
                        background-color: #f0f2f6;
                    }
                    .sidebar .sidebar-content .block-container {
                        padding-top: 2rem;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            selection = st.radio(
                "Go to",
                list(pages.keys()),
                key='navigation'
            )

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
