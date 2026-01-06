import streamlit as st
import pandas as pd

st.set_page_config(page_title="專業爆品搜尋器", layout="wide")

# 載入數據
@st.cache_data
def get_data():
    try:
        return pd.read_csv("data.csv")
    except:
        return pd.DataFrame(columns=["平台", "品名", "熱度", "銷量", "更新日期"])

df = get_data()

st.title("🛡️ 專業電商爆品監控")

# 搜尋框
search_query = st.text_input("🔍 輸入關鍵字搜尋真實爆品 (例如：行動電源)", "")

if search_query:
    # 真實過濾邏輯：只顯示品名中包含關鍵字的結果
    result_df = df[df['品名'].str.contains(search_query, case=False, na=False)]
    
    if not result_df.empty:
        st.subheader(f"找到 {len(result_df)} 筆關於「{search_query}」的真實數據")
        
        # 使用表格顯示完整名稱
        st.dataframe(
            result_df.sort_values(by="熱度", ascending=False),
            column_config={
                "品名": st.column_config.TextColumn("商品完整名稱", width="large"),
                "平台": st.column_config.TextColumn("來源"),
                "熱度": st.column_config.ProgressColumn("爆品熱度", format="%d%%", min_value=0, max_value=100)
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning(f"目前資料庫中尚無關於「{search_query}」的真實數據。")
        st.info("提示：這可能是因為今天的自動爬蟲尚未抓取到該品項，您可以嘗試搜尋『行動電源』或『Anker』。")
else:
    st.subheader("🔥 今日全平台熱銷榜單")
    st.dataframe(df, use_container_width=True, hide_index=True)
