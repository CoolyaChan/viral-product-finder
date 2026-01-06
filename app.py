import streamlit as st
import pandas as pd

st.set_page_config(page_title="全球電商爆品綜合評比", layout="wide")

@st.cache_data
def load_global_data():
    try:
        df = pd.read_csv("data.csv")
        # 如果沒有日期，補上今日
        if '更新日期' not in df.columns:
            df['更新日期'] = "2024-01-01"
        return df
    except:
        return pd.DataFrame(columns=["平台", "品名", "熱度", "銷量", "類別", "更新日期"])

df = load_global_data()

# --- 側邊欄：自動化篩選 (不鎖死) ---
st.sidebar.header("🔍 綜合篩選")

# 自動從數據中提取現有的所有平台與類別
available_platforms = ["全部"] + sorted(df["平台"].unique().tolist())
available_categories = ["全部"] + sorted(df["類別"].unique().tolist())

selected_platform = st.sidebar.selectbox("來源平台評比", available_platforms)
selected_category = st.sidebar.selectbox("商品類別篩選", available_categories)
min_score = st.sidebar.slider("最低綜合爆品得分", 0, 100, 0)

# --- 主介面 ---
st.title("🌎 全球電商爆品大數據評比")
st.caption("整合 Amazon, eBay, 1688, momo, 蝦皮等平台，進行全自動數據綜合分析")

search_query = st.text_input("📝 輸入任意關鍵字進行全域模糊搜尋 (例如：USB、收納、戶外)", "")

# --- 核心邏輯：全域綜合過濾 ---
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['品名'].str.contains(search_query, case=False, na=False)]

if selected_platform != "全部":
    filtered_df = filtered_df[filtered_df['平台'] == selected_platform]

if selected_category != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_category]

filtered_df = filtered_df[filtered_df['熱度'] >= min_score]

# --- 綜合評比顯示 ---
st.subheader(f"📊 綜合評比結果 ({len(filtered_df)} 筆)")

if not filtered_df.empty:
    # 按照熱度進行全平台總排行
    display_df = filtered_df.sort_values(by="熱度", ascending=False)
    
st.dataframe(
        display_df,
        column_config={
            "平台": st.column_config.TextColumn("來源平台"),
            "品名": st.column_config.TextColumn("完整商品名稱", width="large"),
            "熱度": st.column_config.ProgressColumn("綜合爆品得分", format="%d分", min_value=0, max_value=100),
            "銷量": st.column_config.NumberColumn("全網推估銷量"),
            "類別": st.column_config.TextColumn("類別"), # 這裡將 TagColumn 改為 TextColumn
        },
        hide_index=True,
        use_container_width=True
    )
    )
else:
    st.warning("查無數據，請嘗試調整篩選條件或等待自動爬蟲累積更多資料。")
