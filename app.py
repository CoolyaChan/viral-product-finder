import streamlit as st
import pandas as pd

# --- 網頁配置 ---
st.set_page_config(page_title="專業爆品搜尋器", layout="wide")

# --- 數據載入 ---
@st.cache_data
def get_data():
    try:
        df = pd.read_csv("data.csv")
        # 確保類別欄位存在，若無則填入"未分類"
        if '類別' not in df.columns:
            df['類別'] = "未分類"
        return df
    except:
        # 初始空白數據框架
        return pd.DataFrame(columns=["平台", "品名", "熱度", "銷量", "更新日期", "類別"])

df = get_data()

# --- 側邊欄：篩選器區域 ---
st.sidebar.header("🎯 篩選工具")

# 1. 平台篩選
all_platforms = ["全部"] + list(df["平台"].unique())
selected_platform = st.sidebar.selectbox("選擇平台", all_platforms)

# 2. 類別篩選 (這就是你要的類別選單)
all_categories = ["全部"] + list(df["類別"].unique())
selected_category = st.sidebar.selectbox("選擇類別", all_categories)

# 3. 熱度範圍篩選
heat_range = st.sidebar.slider("最低熱度值", 0, 100, 0)

# --- 主畫面：搜尋與結果 ---
st.title("🛡️ 專業電商爆品監控中心")

# 搜尋欄 (與篩選器並用)
search_query = st.text_input("🔍 輸入關鍵字搜尋完整品名 (例如：行動電源、iPhone、露營)", "")

# --- 過濾邏輯 (核心運算) ---
filtered_df = df.copy()

# A. 套用關鍵字搜尋
if search_query:
    filtered_df = filtered_df[filtered_df['品名'].str.contains(search_query, case=False, na=False)]

# B. 套用平台篩選
if selected_platform != "全部":
    filtered_df = filtered_df[filtered_df['平台'] == selected_platform]

# C. 套用類別篩選
if selected_category != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_category]

# D. 套用熱度篩選
filtered_df = filtered_df[filtered_df['熱度'] >= heat_range]

# --- 顯示結果 ---
st.subheader(f"📊 篩選結果 ({len(filtered_df)} 筆)")

if not filtered_df.empty:
    st.dataframe(
        filtered_df.sort_values(by="熱度", ascending=False),
        column_config={
            "品名": st.column_config.TextColumn("商品完整名稱", width="large"),
            "平台": st.column_config.TextColumn("來源平台"),
            "熱度": st.column_config.ProgressColumn("爆品熱度", format="%d%%", min_value=0, max_value=100),
            "銷量": st.column_config.NumberColumn("推估銷量", format="%d"),
            "類別": st.column_config.TextColumn("類別標籤")
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.warning("查無符合條件的數據，請嘗試更換關鍵字或調整篩選器。")

# 頁尾資訊
st.divider()
st.caption(f"數據最後更新：{df['更新日期'].max() if not df.empty else '尚未更新'}")
