"""
World Happiness Report 2015 - Interactive Dashboard & Analytics
Main application entry point for Streamlit Cloud and local execution.
"""

import os
import sys
import runpy

# Determine the path to app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
app_file = os.path.join(current_dir, "app.py")

if __name__ == "__main__":
    # Execute the interactive Streamlit dashboard
    if os.path.exists(app_file):
        runpy.run_path(app_file, run_name="__main__")
    else:
        import streamlit as st
        st.error("Error: app.py not found in the project directory.")
