import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# 頁面配置
st.set_page_config(page_title="Aesop | Digital Lab", layout="centered")

# Aesop 2026 進階視覺規格 — 小而細長標籤版
st.markdown("""
    <style>
    /* 全域背景：調整為更有質感的陶土米色 */
    .stApp {
        background-color: #EAE2D6 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 字體設定：強制使用優雅的襯線字體 */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: "Optima", "Palatino Linotype", "Palatino", "URW Palladio L", "serif" !important;
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
        color: #333333 !important;
    }

    /* 輸入框優化 */
    .stTextInput>div>div>input {
        background-color: #F7F5F0 !important;
        color: #333333 !important;
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

    /* 生產按鈕 (EXPORT)：模擬官網全黑細框 */
    .stButton>button {
        border-radius: 0px !important;
        border: 0.5px solid #333333 !important;
        background-color: #333333 !important;
        color: #EAE2D6 !important;
        width: 100% !important;
        height: 3.8rem !important;
        letter-spacing: 0.2em !important;
        font-size: 0.85rem !important;
        margin-top: 2.5rem;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background-color: #EAE2D6 !important;
        color: #333333 !important;
        border: 0.5px solid #333333 !important;
    }

    /* 模擬白色標籤卡片概念 */
    .label-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 2px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
        text-align: right; /* 讓條碼和下方文字居右 */
    }
    
    /* 條碼下方精緻文字 */
    .label-barcode-text {
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        color: #333333;
        line-height: 1.4;
        margin-top: -10px; /* 緊貼條碼下方 */
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
        # 使用最通用的 Code 128 標準
        BARCODE_CLASS = barcode.get_barcode_class("code128")
        rv = BytesIO()
        
        # 調整條碼參數：細長、變小，且不生成預設文字
        my_barcode = BARCODE_CLASS(val, writer=ImageWriter())
        my_barcode.write(rv, options={
            "write_text": False, 
            "background": "#FFFFFF", # 將條碼生成背景改為白色，放進卡片內
            "module_height": 20.0,  # 顯著增加高度 (維持細長)
            "module_width": 0.10,   # 顯著縮減寬度 (做小一點)
            "quiet_zone": 1.5
        })
        
        # 顯示預覽：利用佈局讓白色卡片靠右下角
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1]) # 中間佔 2/4
        with col2:
            # 在中間列內再分兩列，將白色卡片放在右半邊
            sub_col1, sub_col2 = col2.columns([1, 1])
            with sub_col2:
                st.markdown('<div class="label-card">', unsafe_allow_html=True)
                st.image(rv) # 條碼佔中間列的右半邊，看起來變小了。
                # 手動創建精緻的 Aesop 下方文字
                st.markdown(f'<p class="label-barcode-text">ID: {val}<br>MELBOURNE AUSTRALIA</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 生成下載按鈕 (EXPORT IMAGE)
            st.download_button(
                label="EXPORT BARCODE IMAGE",
                data=rv.getvalue(),
                file_name=f"aesop_label_{val}.png",
                mime="image/png"
            )
    except:
        st.error("輸入格式有誤，無法生成。")

st.caption("Internal Use Only — Aesop Digital Infrastructure")
