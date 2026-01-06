import streamlit as st
import pandas as pd

st.set_page_config(page_title="全球電商爆品綜合評比", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except:
        return pd.DataFrame(columns=["平台", "品名", "熱度", "銷量", "類別", "更新日期"])

df = load_data()

# --- 側邊欄：強制顯示所有選單 ---
st.sidebar.header("🎯 綜合篩選工具")

# 手動定義全平台，不讓它動態消失
all_platforms = ["全部", "蝦皮", "momo", "Amazon", "1688", "淘寶", "PChome", "eBay"]
selected_platform = st.sidebar.selectbox("來源平台評比", all_platforms)

# 手動定義全類別
all_categories = ["全部", "3C數碼", "居家生活", "美妝保養", "戶外運動", "服飾鞋包", "母嬰用品"]
selected_category = st.sidebar.selectbox("商品類別篩選", all_categories)

min_score = st.sidebar.slider("最低綜合爆品得分", 0, 100, 0)

# --- 主畫面 ---
st.title("🌎 全球電商爆品大數據評比")
search_query = st.text_input("🔍 輸入關鍵字進行全域搜尋", "")

# 過濾邏輯
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['品名'].str.contains(search_query, case=False, na=False)]
if selected_platform != "全部":
    filtered_df = filtered_df[filtered_df['平台'] == selected_platform]
if selected_category != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_category]
filtered_df = filtered_df[filtered_df['熱度'] >= min_score]

st.subheader(f"📊 篩選結果 ({len(filtered_df)} 筆)")
st.dataframe(
    filtered_df.sort_values(by="熱度", ascending=False),
    column_config={"品名": st.column_config.TextColumn("完整商品名稱", width="large")},
    hide_index=True, use_container_width=True
)
