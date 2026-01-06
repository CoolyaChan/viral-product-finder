import streamlit as st
import pandas as pd

# --- 網頁配置：設定寬版顯示與標題 ---
st.set_page_config(page_title="全球電商爆品大數據評比", layout="wide")

# --- 數據載入函數 (包含快取機制) ---
@st.cache_data
def load_global_data():
    try:
        # 讀取 GitHub Actions 產生的 data.csv
        df = pd.read_csv("data.csv")
        
        # 基礎欄位檢查，確保資料庫格式正確
        required_columns = ["平台", "品名", "熱度", "銷量", "類別", "更新日期"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = "N/A"
        return df
    except Exception as e:
        # 如果檔案不存在，回傳一個空的框架
        return pd.DataFrame(columns=["平台", "品名", "熱度", "銷量", "類別", "更新日期"])

# 執行載入數據
df = load_global_data()

# --- 側邊欄：動態篩選區域 (自動根據數據生成選單) ---
st.sidebar.header("🎯 綜合篩選工具")

# 自動提取現有的平台與類別清單
available_platforms = ["全部"] + sorted(df["平台"].unique().tolist()) if not df.empty else ["全部"]
available_categories = ["全部"] + sorted(df["類別"].unique().tolist()) if not df.empty else ["全部"]

# 建立選單
selected_platform = st.sidebar.selectbox("來源平台評比", available_platforms)
selected_category = st.sidebar.selectbox("商品類別篩選", available_categories)
min_score = st.sidebar.slider("最低綜合爆品得分", 0, 100, 0)

# --- 主畫面：標題與搜尋 ---
st.title("🌎 全球電商爆品大數據評比系統")
st.info("整合 Amazon, eBay, momo, PChome 等平台，每日自動分析最新爆款趨勢。")

# 關鍵字搜尋欄 (全域模糊搜尋)
search_query = st.text_input("📝 輸入任意關鍵字搜尋 (例如：行動電源、iPhone、露營、USB)", "")

# --- 核心邏輯：過濾數據 ---
filtered_df = df.copy()

# 1. 處理關鍵字搜尋
if search_query:
    filtered_df = filtered_df[filtered_df['品名'].str.contains(search_query, case=False, na=False)]

# 2. 處理平台篩選
if selected_platform != "全部":
    filtered_df = filtered_df[filtered_df['平台'] == selected_platform]

# 3. 處理類別篩選
if selected_category != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_category]

# 4. 處理熱度門檻
filtered_df = filtered_df[filtered_df['熱度'] >= min_score]

# --- 顯示結果表格 ---
st.subheader(f"📊 綜合分析結果 (共 {len(filtered_df)} 筆)")

if not filtered_df.empty:
    # 按照熱度(綜合得分)排序
    display_df = filtered_df.sort_values(by="熱度", ascending=False)
    
    # 顯示表格 (使用相容性最高的 TextColumn)
    st.dataframe(
        display_df,
        column_config={
            "平台": st.column_config.TextColumn("來源平台"),
            "品名": st.column_config.TextColumn("完整商品名稱", width="large"),
            "熱度": st.column_config.ProgressColumn("綜合爆品得分", format="%d分", min_value=0, max_value=100),
            "銷量": st.column_config.NumberColumn("推估銷量"),
            "類別": st.column_config.TextColumn("類別標籤"),
            "更新日期": st.column_config.TextColumn("採集時間")
        },
        hide_index=True,
        use_container_width=True
    )
else:
    # 查無資料時的提示
    if df.empty:
        st.warning("⚠️ 資料庫目前是空的。請確保 GitHub Actions 的爬蟲任務已成功執行並產生了 data.csv 檔案。")
    else:
        st.warning("🔍 查無符合條件的數據，請更換關鍵字或放寬篩選條件。")

# --- 頁尾 ---
st.divider()
last_update = df['更新日期'].max() if not df.empty else "未知"
st.caption(f"系統狀態：運行中 | 數據採集頻率：每日一次 | 最後數據更新時間：{last_update}")
