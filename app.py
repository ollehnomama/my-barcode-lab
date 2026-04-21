import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# 頁面配置
st.set_page_config(page_title="Aesop | Digital Lab", layout="centered")

# Aesop 2026 進階視覺規格
st.markdown("""
    <style>
    /* 全域背景：骨瓷白 */
    .stApp {
        background-color: #FFFCF7 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: "Palatino Linotype", "Palatino", "serif" !important;
        color: #333333 !important;
    }

    /* 標題設定 */
    h1 {
        font-weight: 200 !important;
        letter-spacing: 0.25em !important;
        text-transform: uppercase;
        font-size: 1.2rem !important;
        padding-top: 4rem !important;
        margin-bottom: 3rem !important;
    }

    /* 輸入框優化：解決輸入時看不清楚的問題 */
    .stTextInput>div>div>input {
        background-color: #F7F5F0 !important; /* 稍微深一點的背景色增加輸入時的對比 */
        color: #333333 !important; /* 強制文字顏色為深色 */
        border-radius: 0px !important;
        border: none !important;
        border-bottom: 0.5px solid #333333 !important;
        font-size: 1rem !important;
        padding: 18px 12px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        background-color: #FFFFFF !important;
        box-shadow: none !important;
        border-bottom: 1px solid #333333 !important;
    }

    /* 漂亮的工作按鈕：模擬官網的高級質感 */
    .stButton>button {
        border-radius: 0px !important;
        border: 0.5px solid #333333 !important;
        background-color: #333333 !important;
        color: #FFFCF7 !important;
        width: 100% !important;
        height: 3.8rem !important;
        letter-spacing: 0.2em !important;
        font-size: 0.85rem !important;
        margin-top: 2.5rem;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background-color: #FFFCF7 !important;
        color: #333333 !important;
        border: 0.5px solid #333333 !important;
    }

    .stCaption {
        font-size: 0.65rem !important;
        letter-spacing: 0.1em !important;
        color: #999 !important;
        margin-top: 8rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Inventory Management Tool")

# 獲取輸入
val = st.text_input("", placeholder="請在此輸入編號 (按下 Enter 預覽)")

if val:
    try:
        # 使用 Code 128 標準
        BARCODE_CLASS = barcode.get_barcode_class("code128")
        rv = BytesIO()
        
        # 調整條碼比例：增加 module_height 讓它變得細長
        my_barcode = BARCODE_CLASS(val, writer=ImageWriter())
        my_barcode.write(rv, options={
            "write_text": False, 
            "background": "#FFFCF7",
            "module_height": 20.0,  # 顯著增加高度
            "module_width": 0.18,   # 稍微縮減寬度以維持優雅
            "quiet_zone": 1.5
        })
        
        # 顯示預覽
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 4, 1]) # 中間區塊拉寬
        with col2:
            st.image(rv, use_container_width=True)
            st.write(f"<p style='text-align:center; letter-spacing:0.4em; font-size:0.65rem; color:#A1A1A1; margin-top:10px;'>{val}</p>", unsafe_allow_html=True)
            
            # 生成下載按鈕
            st.download_button(
                label="GENERATE BARCODE IMAGE",
                data=rv.getvalue(),
                file_name=f"label_{val}.png",
                mime="image/png"
            )
    except:
        st.error("輸入格式有誤，無法生成。")

st.caption("Internal Use Only — Aesop Digital Infrastructure")
