import streamlit as st
import pandas as pd

st.set_page_config(page_title="爆品搜尋器", layout="wide")

st.title("🚀 全球電商爆品熱度監控器")
st.caption("數據每日自動更新，協助您精準選品")

# 讀取數據
try:
    df = pd.read_csv("data.csv")
except:
    st.warning("數據初始化中，請稍後...")
    df = pd.DataFrame(columns=["平台", "品名", "銷量", "熱度", "更新日期"])

# 側邊欄：篩選器
st.sidebar.header("篩選條件")
platforms = st.sidebar.multiselect("選擇平台", options=df["平台"].unique(), default=df["平台"].unique())
min_heat = st.sidebar.slider("最低熱度值", 0, 100, 50)

# 主畫面：搜尋欄
search_query = st.text_input("🔍 輸入關鍵字搜尋（例如：手機殼、筋膜槍）", "")

# 數據過濾邏輯
filtered_df = df[
    (df["平台"].isin(platforms)) & 
    (df["熱度"] >= min_heat) & 
    (df["品名"].str.contains(search_query, case=False, na=False))
]

# 顯示結果
st.subheader(f"找到 {len(filtered_df)} 筆熱銷商品")
st.dataframe(filtered_df.sort_values(by="熱度", ascending=False), use_container_width=True)

# 爆品公式說明
with st.expander("📊 如何計算熱度？"):
    st.write("熱度值是基於以下權重計算得出：")
    st.latex(r"HeatScore = (Sales \times 0.6) + (GrowthRate \times 0.4)")
