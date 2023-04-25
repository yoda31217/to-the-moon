import streamlit as st
from report.report import build_report

try:
    build_report()

except Exception as e:
    st.error(f"Ошибка: {str(e)}", icon="🚨")
