import streamlit as st
import base64
import os


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None


def _footer(color="white"):
    image_path = "dmlogo.png"
    img_base64 = get_base64_image(image_path)
    logo_html = f"data:image/png;base64,{img_base64}" if img_base64 else ""
    st.markdown(
        f"""
        <div style="margin-top:2rem; display:flex; gap:8px; justify-content:center; align-items:center;">
            <p style="font-weight:bold; color:{color}; margin:0;">Created with ❤️ by</p>
            <img src="{logo_html}" style="max-height:85px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_home():
    _footer(color="white")


def footer_dashboard():
    _footer(color="black")
