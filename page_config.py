import base64
import os
import tempfile
import requests
import streamlit as st
from pathlib import Path

# obtain catalogue files from GitHub repository https://github.com/soler-he/catalogues
BASE_URL = "https://raw.githubusercontent.com/soler-he/catalogues/main/"

CATALOGUE_DIR = Path(tempfile.gettempdir()) / 'catalogues'

CATALOGUE_FILES = [
    'SOLER_CME_catalogue.csv',
    'SOLER_Flare_catalogue.csv',
    'SOLER_SEP_catalogue.csv',
]


@st.cache_resource(show_spinner=False)  # runs once per app session, not once per page/rerun
def download_catalogues():
    CATALOGUE_DIR.mkdir(exist_ok=True)
    failed = []
    for fname in CATALOGUE_FILES:
        fpath = CATALOGUE_DIR / fname
        if not fpath.exists():
            try:
                response = requests.get(f'{BASE_URL}{fname}', timeout=10)
                response.raise_for_status()
                fpath.write_text(response.text, encoding='utf-8')
                print(f"{fname}: downloaded successfully to {fpath}")
            except Exception as e:
                failed.append((fname, str(e)))
                print(f"{fname}: download failed ({e})")
        else:
            print(f"{fname}: already exists at {fpath} (skipped)")
    return failed  # return failures instead of calling st.stop() here


def setup():
    download_catalogues()  # cached — only downloads once, but guaranteed to run first
    st.set_page_config(
        page_title="SOLER Catalogues",
        page_icon="images/SOLER_Favicon-150x150.png",  # "☀️",  # 🔆
        layout="wide",
        initial_sidebar_state="collapsed",
        # menu_items={
        #     'Get Help': 'https://www.extremelycoolapp.com/help',
        #     'Report a bug': "https://www.extremelycoolapp.com/bug",
        #     'About': "# This is a header. This is an *extremely* cool app!"
        # }
    )
    # st.logo("images/soler.png", size='large')

    # for my_key in ["selected_columns_1", "selected_columns_2"]:
    #     if my_key in st.session_state:
    #         st.session_state[my_key] = st.session_state[my_key]

    # st.sidebar.checkbox("Expand columns to show content", value=True, key='fitCellContents')

    # available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material", "quartz",  "alpine"]
    # selected_theme = st.sidebar.selectbox("Theme", available_themes, key='selected_theme')

    # st.sidebar.write(st.session_state)

    pages = [st.Page("pages/home.py", title="Home"),
             st.Page("pages/cme_catalogue.py", title="CME catalogue"),
             st.Page("pages/flare_catalogue.py", title="Flare catalogue"),
             st.Page("pages/sep_catalogue.py", title="SEP catalogue"),
             ]

    pg = st.navigation(pages, position="top")
    # pg.run()

    st.markdown(
        """
            <style>
                    .stMainBlockContainer {
                        # padding-left: 0rem;
                        # padding-right: 0rem;
                        padding-top: 4rem;
                        padding-bottom: 0rem;
                    }
                    # .stAppHeader {
                    #     background-color: rgba(255, 255, 255, 0.0);
                    #     visibility: visible;
                    # }
                    # [data-testid = "stSidebarHeader"] {
                    #     height: 2rem; /* 2rem keeps just enough space for the icon*/
                    # }
            </style>
            """,
        unsafe_allow_html=True,
    )

    return pg


def get_download_link(fname: str, link_text: str) -> str:
    file_path = CATALOGUE_DIR / fname
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{fname}">{link_text}</a>'
    return href
