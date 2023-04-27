from venv import logger
import streamlit as st
from report.report import build_report

try:
    build_report()

except Exception as e:
    logger.error("Unknown error occured.", e)
    st.error(f"Ошибка: {str(e)}", icon="🚨")
