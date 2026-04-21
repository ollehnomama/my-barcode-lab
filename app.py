import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# 頁面風格自定義
st.set_page_config(page_title="Barcode Lab", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F1F0E8; } /* Aesop 風格背景 */
    input { border-radius: 0px !important; border-bottom: 1px solid #333 !important; }
    .stButton>button { border-radius: 0px; border: 1px solid #333; background-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

st.title("純生產條碼工具")
st.write("輸入數值後，Enter 即可生成。")

# 預設為最通用的 Code 128
val = st.text_input("輸入編號", placeholder="例如：9319944002355")

if val:
    try:
        BARCODE_CLASS = barcode.get_barcode_class("code128")
        rv = BytesIO()
        # write_text=True 會在條碼下方顯示數字，方便對照
        my_barcode = BARCODE_CLASS(val, writer=ImageWriter())
        my_barcode.write(rv, options={"write_text": True, "font_size": 10})
        
        # 預覽與下載
        st.image(rv, width=350)
        st.download_button(
            label="下載 PNG 圖片",
            data=rv.getvalue(),
            file_name=f"barcode_{val}.png",
            mime="image/png"
        )
    except:
        st.error("輸入格式有誤")
