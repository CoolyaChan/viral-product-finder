import streamlit as st
import pandas as pd
import random

# --- 網頁配置 ---
st.set_page_config(page_title="全球電商爆品搜尋器", layout="wide")

# --- 自定義樣式 ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 數據載入函數 ---
@st.cache_data
def load_historical_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except:
        # 如果還沒產生 data.csv，回傳一個空的框架
        return pd.DataFrame(columns=["平台", "品名", "銷量", "熱度", "更新日期", "類別"])

# --- 模擬即時搜尋引擎 (針對自由輸入) ---
def mock_live_search(keyword, platforms):
    live_results = []
    for p in platforms:
        # 這裡模擬針對特定關鍵字的熱度計算
        for i in range(3):
            heat = random.randint(60, 99)
            live_results.append({
                "平台": p,
                "品名": f"{keyword} - {p}熱銷款_{i+1}",
                "熱度": heat,
                "銷量推估": random.randint(100, 10000),
                "競爭程度": "高" if heat > 85 else "中"
            })
    return pd.DataFrame(live_results)

# --- 主介面 ---
st.title("🛡️ 全球電商爆品監控中心")
st.info("本工具整合 GitHub Actions 每日自動採集之數據，並支援全平台關鍵字分析。")

# 側邊欄控制
st.sidebar.header("控制面板")
all_platforms = ["蝦皮", "momo", "Amazon", "eBay", "1688", "淘寶", "PChome"]
selected_platforms = st.sidebar.multiselect("選擇搜尋範圍", all_platforms, default=["蝦皮", "momo", "Amazon"])

# --- 第一區塊：自由搜尋欄 ---
search_query = st.text_input("🔍 輸入商品關鍵字 (如：筋膜槍、露營燈、洗臉機)", "")

if search_query:
    st.subheader(f"分析結果：{search_query}")
    
    # 執行搜尋邏輯
    search_df = mock_live_search(search_query, selected_platforms)
    
    # 顯示指標卡
    col1, col2, col3 = st.columns(3)
    avg_heat = int(search_df['熱度'].mean())
    col1.metric("平均市場熱度", f"{avg_heat}%", delta="趨勢上升")
    col2.metric("競爭激烈度", "極高" if avg_heat > 80 else "中等")
    col3.metric("建議毛利", "30% - 45%")

    # 分平台展示結果
    tabs = st.tabs(selected_platforms)
    for i, tab in enumerate(tabs):
        with tab:
            p_name = selected_platforms[i]
            p_data = search_df[search_df['平台'] == p_name]
            st.table(p_data[["品名", "熱度", "銷量推估", "競爭程度"]])
            st.button(f"前往 {p_name} 查看真實搜尋結果", key=f"btn_{p_name}")

else:
    # --- 第二區塊：每日爆品排行榜 (當沒搜尋時顯示) ---
    st.divider()
    st.subheader("🔥 今日各平台爆品排行 (自動更新)")
    
    db_df = load_historical_data()
    
    if not db_df.empty:
        # 按平台過濾
        filtered_db = db_df[db_df['平台'].isin(selected_platforms)]
        st.dataframe(filtered_db.sort_values(by="熱度", ascending=False), use_container_width=True)
    else:
        st.warning("目前資料庫中尚無排行數據，請檢查 GitHub Actions 是否已成功執行並產生 data.csv。")

# --- 頁尾 ---
st.divider()
st.caption("數據來源：跨平台自動化爬蟲機器人 | 最後更新時間：每日凌晨 04:00")
