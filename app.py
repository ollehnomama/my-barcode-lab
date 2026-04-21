import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# 頁面配置
st.set_page_config(page_title="Aesop | Digital Lab", layout="centered")

# 重新定義極簡美學：精確、留白、比例協調
st.markdown("""
    <style>
    /* 背景改為官網那種清爽的骨瓷色 */
    .stApp {
        background-color: #FFFCF7 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 襯線體字體 */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: "Palatino Linotype", "Palatino", "serif" !important;
        color: #333333 !important;
    }

    /* 標題：極小、優雅、大字距 */
    h1 {
        font-weight: 200 !important;
        letter-spacing: 0.3em !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        padding-top: 3rem !important;
        text-align: center;
        color: #666 !important;
    }

    /* 輸入框：完全去背，只留一條細線 */
    .stTextInput>div>div>input {
        background-color: transparent !important;
        color: #333333 !important;
        border-radius: 0px !important;
        border: none !important;
        border-bottom: 0.5px solid #D1D1D1 !important;
        font-size: 1rem !important;
        text-align: center;
        padding: 10px 0px !important;
    }
    
    /* 模擬白色小標籤卡片 */
    .label-card {
        background-color: #FFFFFF;
        padding: 40px 20px;
        border: 0.5px solid #EAEAEA;
        margin: 2rem auto;
        max-width: 320px; /* 限制寬度，不讓條碼爆開 */
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .barcode-id {
        font-size: 0.75rem;
        letter-spacing: 0.3em;
        margin-top: 15px;
        color: #333;
    }
    
    .location-text {
        font-size: 0.6rem;
        letter-spacing: 0.15em;
        color: #999;
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* 按鈕：細線條與簡約設計 */
    .stButton>button {
        border-radius: 0px !important;
        border: 0.5px solid #333333 !important;
        background-color: #333333 !important;
        color: #FFFCF7 !important;
        width: 100% !important;
        max-width: 320px;
        margin: 0 auto;
        display: block;
        height: 3rem !important;
        letter-spacing: 0.1em !important;
        font-size: 0.75rem !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FFFCF7 !important;
        color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Inventory System")

# 輸入框置中
col_in1, col_in2, col_in3 = st.columns([1, 2, 1])
with col_in2:
    val = st.text_input("", placeholder="Enter Code")

if val:
    try:
        # 條碼規格：這次把 module_height 縮小，讓它變精緻
        BARCODE_CLASS = barcode.get_barcode_class("code128")
        rv = BytesIO()
        my_barcode = BARCODE_CLASS(val, writer=ImageWriter())
        my_barcode.write(rv, options={
            "write_text": False, 
            "background": "#FFFFFF",
            "module_height": 12.0,  # 縮短高度
            "module_width": 0.15,   # 縮窄寬度
            "quiet_zone": 1.0
        })
        
        # 顯示白色標籤卡片
        st.markdown(f"""
            <div class="label-card">
                <img src="data:image/png;base64,{st.image(rv, output_format='PNG', width=220)}" style="display:none;">
                <div class="barcode-id">ID: {val}</div>
                <div class="location-text">Melbourne Australia</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 使用原生 Streamlit 顯示圖片以確保下載功能
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(rv, width=220) # 這裡強制限制寬度
            
            st.download_button(
                label="EXPORT IMAGE",
                data=rv.getvalue(),
                file_name=f"label_{val}.png",
                mime="image/png"
            )
    except:
        st.error("Invalid Code")

st.markdown("<div style='margin-top: 5rem; text-align: center; font-size: 0.5rem; color: #CCC;'>INTERNAL USE ONLY</div>", unsafe_allow_html=True)
