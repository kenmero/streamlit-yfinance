import streamlit as st
import params as pm
import utils

st.title('米国株価可視化アプリ')

################################
# サイドバーを定義
################################
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write('## 表示日数選択')
days = st.sidebar.slider('日数',1, 50, pm.days)

st.sidebar.write('## 株価の範囲指定')
y_min, y_max = st.sidebar.slider('範囲を指定してください。', 
                                 0.0, 3500.0, (pm.y_min, pm.y_max))

################################
# body部を定義
################################
st.write(f'### 過去 **{days}日間** のGAFAの株価')

companies = st.multiselect('会社名を選択してください', 
                           pm.tickers.keys(),
                           ['google', 'amazon', 'facebook', 'apple']
                           )
if not companies:
    st.error('少なくとも1社は選んでください。')
else:
    try:
        t_tickers = utils.get_target_tickers(pm.tickers, companies)
        df = utils.get_data(t_tickers, days=days)
        st.write('### 株価(USD)', df)

        shape_data = utils.shaping_data(df)
        chart = utils.drawing(shape_data, y_min, y_max)
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(
            f'描画処理中にエラーが発生しました。詳細：class「{e.__class__}」message「{e}」'
        )



