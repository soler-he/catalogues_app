import streamlit as st
from page_config import setup, download_catalogues

pg = setup()

with st.spinner("Downloading catalogues, please wait..."):
    failed = download_catalogues()

if failed:
    download_catalogues.clear()
    msg = "**Failed to download the following catalogues:**\n"
    for fname, reason in failed:
        msg += f"- `{fname}`: {reason}\n"
    msg += "\nPlease reload the page. If the problem persists, the catalogue server may be temporarily unavailable."
    st.error(msg)
    st.stop()

pg.run()
