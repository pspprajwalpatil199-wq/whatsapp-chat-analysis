import streamlit as st
import preprocessor, helper

# ✅ CSS Styling
st.markdown("""
<style>
.metric-box {
    border: 2px solid #444;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    background-color: #111;
}
.metric-title {
    font-size: 20px;
    color: #ccc;
}
.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ✅ Sidebar
st.sidebar.title("Whatsapp Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocessor(data)
    st.dataframe(df)

    # ✅ User list
    user_list = df['user'].unique().tolist()
    if "group notification" in user_list:
        user_list.remove("group notification")

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis", user_list)

    # ✅ BUTTON CONTROL
    if st.sidebar.button("Show analysis"):

        # =======================
        # 🔥 TOP STATISTICS
        # =======================
        num_message, words, media, links = helper.fetch_stats(selected_user, df)

        st.markdown("""
        <h1 style='text-align: center; color: #00ADB5;'>
        Top Statistics for WhatsApp Chat
        </h1>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Total Messages</div>
                <div class="metric-value">{num_message}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Total Words</div>
                <div class="metric-value">{words}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Media Shared</div>
                <div class="metric-value">{media}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Links Shared</div>
                <div class="metric-value">{links}</div>
            </div>
            """, unsafe_allow_html=True)

        # =======================
        # 📊 MOST BUSY USERS
        # =======================
        if selected_user == "Overall":

            st.markdown("""
            <h2 style='color:#FFD369;'>Most Busy Users</h2>
            """, unsafe_allow_html=True)

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            import matplotlib.pyplot as plt

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='#00ADB5')
                plt.xticks(rotation=45)
                ax.set_title("Top Users")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # =======================
        # 🔤 MOST COMMON WORDS
        # =======================
        st.markdown("""
        <h2 style='color:#FF6F61;'>Most Common Words</h2>
        """, unsafe_allow_html=True)

        common_words = helper.most_common_words(selected_user, df)

        import pandas as pd
        common_df = pd.DataFrame(common_words, columns=['word', 'count'])

        col1, col2 = st.columns(2)

        import matplotlib.pyplot as plt

        with col1:
            fig, ax = plt.subplots()
            ax.bar(common_df['word'], common_df['count'], color='#FF6F61')
            plt.xticks(rotation=45)
            ax.set_title("Top 10 Words")
            st.pyplot(fig)

        with col2:
            st.dataframe(common_df)
