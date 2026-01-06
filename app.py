import streamlit as st
import pandas as pd

st.set_page_config(page_title="全球爆品監控中心", layout="wide")

@st.cache_data
def get_data():
    try:
        df = pd.read_csv("data.csv")
        # 確保必要的欄位都存在
        for col in ["平台", "品名", "熱度", "銷量", "類別"]:
            if col not in df.columns:
                df[col] = "未分類"
        return df
    except:
        return pd.DataFrame(columns=["平台", "品名", "熱度", "銷量", "更新日期", "類別"])

df = get_data()

# --- 側邊欄：強制顯示所有選單 ---
st.sidebar.header("🎯 篩選工具")

# 1. 強制定義全平台清單
full_platform_list = ["全部", "蝦皮", "momo", "Amazon", "1688", "淘寶", "PChome", "eBay"]
selected_platform = st.sidebar.selectbox("選擇平台", full_platform_list)

# 2. 強制定義常用類別 (解決類別不能選的問題)
full_category_list = ["全部", "3C數碼", "居家生活", "美妝保養", "戶外運動", "服飾鞋包", "母嬰用品"]
selected_category = st.sidebar.selectbox("選擇類別", full_category_list)

# 3. 熱度篩選
heat_range = st.sidebar.slider("最低熱度值", 0, 100, 0)

# --- 主畫面 ---
st.title("🛡️ 專業電商爆品監控中心")
search_query = st.text_input("🔍 輸入關鍵字搜尋 (如：行動電源、露營、iPhone)", "")

# 過濾邏輯
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['品名'].str.contains(search_query, case=False, na=False)]
if selected_platform != "全部":
    filtered_df = filtered_df[filtered_df['平台'] == selected_platform]
if selected_category != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_category]
filtered_df = filtered_df[filtered_df['熱度'] >= heat_range]

st.subheader(f"📊 篩選結果 ({len(filtered_df)} 筆)")
st.dataframe(
    filtered_df.sort_values(by="熱度", ascending=False),
    column_config={
        "品名": st.column_config.TextColumn("商品完整名稱", width="large"),
        "熱度": st.column_config.ProgressColumn("爆品熱度", format="%d%%"),
    },
    hide_index=True, use_container_width=True
)
