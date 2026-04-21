import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

# 頁面配置
st.set_page_config(page_title="Aesop | Digital Lab", layout="centered")

# 極簡美學 CSS：只保留一個精緻的卡片
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFCF7 !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: "Palatino Linotype", "Palatino", "serif" !important;
        color: #333333 !important;
    }

    h1 {
        font-weight: 200 !important;
        letter-spacing: 0.3em !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        padding-top: 3rem !important;
        text-align: center;
        color: #666 !important;
    }

    .stTextInput>div>div>input {
        background-color: transparent !important;
        color: #333333 !important;
        border-radius: 0px !important;
        border: none !important;
        border-bottom: 0.5px solid #D1D1D1 !important;
        text-align: center;
        padding: 10px 0px !important;
    }
    
    /* 核心白色標籤：置中、精緻 */
    .label-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #FFFFFF;
        padding: 40px 20px;
        border: 0.5px solid #EAEAEA;
        margin: 2rem auto;
        max-width: 280px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .barcode-id {
        font-size: 0.75rem;
        letter-spacing: 0.3em;
        margin-top: 15px;
        color: #333;
        text-align: center;
    }
    
    .location-text {
        font-size: 0.6rem;
        letter-spacing: 0.15em;
        color: #999;
        margin-top: 5px;
        text-transform: uppercase;
        text-align: center;
    }

    .stButton>button {
        border-radius: 0px !important;
        border: 0.5px solid #333333 !important;
        background-color: #333333 !important;
        color: #FFFCF7 !important;
        width: 100% !important;
        max-width: 280px;
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

# 輸入框
col_in1, col_in2, col_in3 = st.columns([1, 2, 1])
with col_in2:
    val = st.text_input("", placeholder="Enter Code")

if val:
    try:
        # 條碼設定
        BARCODE_CLASS = barcode.get_barcode_class("code128")
        rv = BytesIO()
        my_barcode = BARCODE_CLASS(val, writer=ImageWriter())
        # module_height 設為 12 讓它細長，module_width 0.15 讓它變小
        my_barcode.write(rv, options={
            "write_text": False, 
            "background": "#FFFFFF",
            "module_height": 12.0,
            "module_width": 0.15,
            "quiet_zone": 1.0
        })
        
        # 轉換為 base64 以便在 HTML 顯示，避免重複渲染
        encoded = base64.b64encode(rv.getvalue()).decode()
        
        # 顯示單一標籤卡片
        st.markdown(f"""
            <div class="label-container">
                <img src="data:image/png;base64,{encoded}" width="200">
                <div class="barcode-id">ID: {val}</div>
                <div class="location-text">Melbourne Australia</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 下載按鈕
        st.download_button(
            label="EXPORT IMAGE",
            data=rv.getvalue(),
            file_name=f"label_{val}.png",
            mime="image/png"
        )
    except:
        st.error("Invalid Code")

st.markdown("<div style='margin-top: 5rem; text-align: center; font-size: 0.5rem; color: #CCC;'>INTERNAL USE ONLY</div>", unsafe_allow_html=True)
