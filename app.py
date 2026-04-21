import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# 頁面配置
st.set_page_config(page_title="Aesop | Barcode Tool", layout="centered")

# 官網 1:1 美學 CSS 注入
st.markdown("""
    <style>
    /* 全域背景：改為官網的骨瓷白 #FFFCF7 */
    .stApp {
        background-color: #FFFCF7 !important;
    }
    
    /* 隱藏所有不需要的裝飾 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 字體設定：襯線標題與無襯線內容的平衡 */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: "Palatino Linotype", "Palatino", "serif" !important;
        color: #333333 !important;
        line-height: 1.6;
    }

    /* 標題：極簡、大寫、增加字距 */
    h1 {
        font-weight: 200 !important;
        letter-spacing: 0.2em !important;
        text-transform: uppercase;
        font-size: 1.4rem !important;
        padding-top: 3rem !important;
        margin-bottom: 2rem !important;
        text-align: left;
    }

    /* 輸入框：Aesop 標誌性的極細底線 */
    .stTextInput>div>div>input {
        background-color: transparent !important;
        border-radius: 0px !important;
        border: none !important;
        border-bottom: 0.5px solid #D1D1D1 !important;
        font-size: 1rem !important;
        padding: 15px 0px !important;
        color: #333 !important;
    }
    .stTextInput>div>div>input:focus {
        border-bottom: 0.5px solid #333333 !important;
        box-shadow: none !important;
    }
    
    /* 按鈕：黑底細框，模擬官網購買按鈕 */
    .stButton>button {
        border-radius: 0px !important;
        border: 0.5px solid #333333 !important;
        background-color: #333333 !important;
        color: #FFFCF7 !important;
        width: 100% !important;
        height: 3.5rem !important;
        letter-spacing: 0.15em !important;
        font-size: 0.9rem !important;
        margin-top: 2rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFFCF7 !important;
        color: #333333 !important;
        border: 0.5px solid #333333 !important;
    }

    /* 提示文字細節 */
    .stCaption {
        font-size: 0.7rem !important;
        letter-spacing: 0.05em !important;
        color: #666 !important;
        margin-top: 5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 內容排版：模擬官網頁面結構
st.title("Digital Lab — Barcode")
st.write("探索秩序的本質。")

# 輸入框
val = st.text_input("", placeholder="請輸入產品編號或是貨號")

if val:
    try:
        # 使用 Code 128
        BARCODE_CLASS = barcode.get_barcode_class("code128")
        rv = BytesIO()
        
        # 條碼生成：背景色與網頁底色完全同步
        my_barcode = BARCODE_CLASS(val, writer=ImageWriter())
        my_barcode.write(rv, options={
            "write_text": False, 
            "background": "#FFFCF7", # 同步背景色
            "module_height": 10.0,
            "quiet_zone": 1.0,
            "module_width": 0.2
        })
        
        # 顯示區域
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(rv, use_container_width=True)
            st.write(f"<p style='text-align:center; letter-spacing:0.3em; font-size:0.7rem; color:#888;'>SPECIFICATION: {val}</p>", unsafe_allow_html=True)
            
            # 下載按鈕
            st.download_button(
                label="EXPORT IMAGE",
                data=rv.getvalue(),
                file_name=f"aesop_label_{val}.png",
                mime="image/png"
            )
    except:
        st.error("輸入內容無法生成，請檢查格式。")

# 頁尾：留白與低調資訊
st.caption("© Aesop Operations Optimization — 2026")
