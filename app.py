import streamlit as st
import pandas as pd
import scraper  # 確保與您的 scraper.py 在同一層級
import time

# --- 網頁配置 ---
st.set_page_config(
    page_title="全球電商即時爆品評比",
    page_icon="🛡️",
    layout="wide"
)

# --- 自定義樣式 ---
st.markdown("""
    <style>
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    .stMetric { background-color: #ffffff; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 主畫面標題 ---
st.title("🛡️ 全球電商即時數據監控中心")
st.markdown("本系統是根據您的關鍵字**即時對全球平台發動檢索**。")

# --- 側邊欄：功能選單 ---
st.sidebar.header("🎯 搜尋配置")
selected_platforms = st.sidebar.multiselect(
    "包含平台",
    ["momo", "PChome", "Amazon", "eBay", "1688", "淘寶"],
    default=["momo", "PChome", "Amazon", "eBay", "1688", "淘寶"]
)

st.sidebar.divider()
st.sidebar.info("💡 提示：輸入具體商品名稱（如：筋膜槍）比模糊詞（如：電）效果更好。")

# --- 搜尋輸入區 ---
search_query = st.text_input("🔍 請輸入您想評比的商品關鍵字：", placeholder="例如：行動電源、露營摺疊桌、自動貓砂盆...")

if search_query:
    # 建立搜尋動畫
    with st.spinner(f"正在連線全平台 API 並檢索「{search_query}」的即時行情..."):
        # 調用 scraper.py 中的 fetch_all_platforms 函數
        try:
            raw_results = scraper.fetch_all_platforms(search_query)
            
            if raw_results:
                df = pd.DataFrame(raw_results)
                
                # 根據側邊欄選擇的平台進行過濾
                filtered_df = df[df['平台'].isin(selected_platforms)]
                
                if not filtered_df.empty:
                    # --- 數據展示區 ---
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(f"📊 「{search_query}」全平台數據分析")
                        st.dataframe(
                            filtered_df.sort_values(by="熱度", ascending=False),
                            column_config={
                                "平台": st.column_config.TextColumn("來源平台"),
                                "品名": st.column_config.TextColumn("完整品名", width="large"),
                                "熱度": st.column_config.ProgressColumn("爆品潛力評分", format="%d分", min_value=0, max_value=100),
                                "類別": st.column_config.TextColumn("標籤")
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                    
                    with col2:
                        st.subheader("📈 平台熱度對比")
                        avg_heat = filtered_df.groupby('平台')['熱度'].mean().reset_index()
                        st.bar_chart(avg_heat.set_index('平台'))
                        
                        max_item = filtered_df.loc[filtered_df['熱度'].idxmax()]
                        st.metric("當前最高熱度", f"{max_item['熱度']}分", f"來自 {max_item['平台']}")

                else:
                    st.warning("⚠️ 您選擇的平台目前無相關搜尋結果，請嘗試勾選更多平台。")
            else:
                st.error("❌ 抱歉，目前所有平台皆未回傳數據，可能是請求過於頻繁，請稍後再試。")
        except Exception as e:
            st.error(f"系統執行錯誤: {str(e)}")
            st.info("請檢查 scraper.py 檔案是否與 app.py 放在一起，且 requirements.txt 已安裝必要套件。")

else:
    # 初始歡迎畫面
    st.divider()
    col_a, col_b, col_c = st.columns(3)
    col_a.markdown("### 1. 輸入名稱\n輸入您感興趣的任何商品名稱。")
    col_b.markdown("### 2. 即時爬取\n系統會立刻模擬真人前往各國電商網站抓取。")
    col_c.markdown("### 3. 綜合評比\n自動計算各平台的熱度與競爭力。")
    
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80", caption="Global E-commerce Data Analytics")

# --- 頁尾 ---
st.divider()
st.caption("🔍 本工具僅供研究參考。實時數據受各平台網路限制影響，搜尋結果可能有 3-5 秒延遲。")
