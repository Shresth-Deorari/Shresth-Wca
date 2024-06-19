import streamlit as st
import matplotlib.pyplot as plt
import time
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import Data_Processor
import My_functions
import Keys

names = ["Shresth Deorari", "Nandini Deorari"]
usernames = ["Shresth_38", "Nandini_17"]
passwords = ["13feb2004", "17jan2003"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)


st.title("Whatsapp Chat Analyzer")
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Wrong Username/Password")
if authentication_status == None :
    st.warning("Please Enter Username & Password")
if authentication_status == True:
    st.sidebar.title("Whatsapp Chat Analyzer")
    st.sidebar.subheader(f"Welcome {name}")
    try:
        authenticator.logout("Logout", "sidebar")
    except Exception as e:
        st.error(f"Error during logout: {str(e)}")

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        if not uploaded_file.name.endswith('.txt'):
            st.error("Wrong file uploaded, Please try again")
            st.stop()
        # Section to upload file
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode('utf-8')  # convert to utf-8 text file

        # Convert text file to dataframe using self module Data_Processor
        df = Data_Processor.Preprocessor(data)

        # Extract user list from df and Create dropbox in sidebar
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.sidebar.selectbox("Select User for Chat Analysis", user_list)

        # Create button for starting analysis
        if st.sidebar.button("Start Analysis"):
            # start progress bar
            progress_text = "Analysis in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            st.success('Analysis Complete')

            st.title("Chat Statistics")
            total_messages, total_words, media_count, url_count = My_functions.stats(selected_user, df)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.header("Total Messages")
                st.title(total_messages)
            with col2:
                st.header("Total Words")
                st.title(total_words)
            with col3:
                st.header("Total Media Shared")
                st.title(media_count)
            with col4:
                st.header("Urls Shared")
                st.title(url_count)

            # Timeline of messages
            st.title("Timeline")
            timeline = My_functions.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Find most active users if Overall selected
            if selected_user == 'Overall':
                st.title("Most Active Users")  # Moved the title above the plot
                col5, col6 = st.columns(2)
                most_active, percentage_df = My_functions.Most_Active_Users(df)
                fig, ax = plt.subplots()
                ax.bar(most_active.index, most_active.values, color='purple')
                plt.xticks(rotation='vertical')
                with col5:
                    st.pyplot(fig)
                with col6:
                    st.dataframe(percentage_df)

            # Display Word Cloud for most common words
            st.title("Word Cloud")
            wc_img = My_functions.Create_Word_Cloud(selected_user, df)
            st.image(wc_img)

            # Display top 20 most common words
            st.title("Top 20 Most Used Words")
            common_df = My_functions.most_common_words(selected_user, df)
            common_df.index = range(1, len(common_df) + 1)  # Adjusting index to start from 1
            st.table(common_df)

            # Display top 20 most common emojis
            st.title("Top 20 Most Used Emojis")
            common_emoji = My_functions.Emoji_Analysis(selected_user, df).head(20)  # Get top 20 emojis
            common_emoji.index = range(1, len(common_emoji) + 1)  # Adjusting index to start from 1
            st.table(common_emoji)
