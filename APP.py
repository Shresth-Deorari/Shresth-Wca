import streamlit as st
import matplotlib.pyplot as plt
import time
from sqlalchemy.orm import Session
from database import SessionLocal, User
from werkzeug.security import generate_password_hash, check_password_hash
import Data_Processor
import My_functions

def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db, email):
    return db.query(User).filter(User.email == email).first()

def create_user(db, username, email, password):
    hashed_password = generate_password_hash(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def load_user_data():
    session = SessionLocal()
    users = session.query(User).all()
    names = [user.username for user in users]
    usernames = [user.username for user in users]
    hashed_passwords = [user.hashed_password for user in users]
    return names, usernames, hashed_passwords

def main():
    st.title("Whatsapp Chat Analyzer")

    # Custom CSS to position Sign Up link at the top right
    st.markdown("""
        <style>
        .signup-link {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 16px;
        }
        .forgot-password-link {
            display: block;
            margin-top: 10px;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'auth_action' not in st.session_state:
        st.session_state['auth_action'] = "login"

    if st.session_state['authenticated']:
        st.sidebar.title("Whatsapp Chat Analyzer")
        st.sidebar.subheader(f"Welcome {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['auth_action'] = 'login'
            st.experimental_rerun()

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

    else:
        option = st.radio("Choose an option", ("Login", "Sign Up", "Forgot Password"))

        if option == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                db = SessionLocal()
                user = get_user_by_username(db, username)
                if user and check_password_hash(user.hashed_password, password):
                    st.success("Login successful!")
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                else:
                    st.error("Invalid username or password")

        elif option == "Sign Up":
            new_username = st.text_input("New Username")
            new_email = st.text_input("New Email")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Sign Up"):
                if new_password == confirm_password:
                    db = SessionLocal()
                    if get_user_by_username(db, new_username):
                        st.error("Username already exists")
                    elif get_user_by_email(db, new_email):
                        st.error("Email already exists")
                    else:
                        create_user(db, new_username, new_email, new_password)
                        st.success("User created successfully!")
                        st.session_state['auth_action'] = "login"
                else:
                    st.error("Passwords do not match")

        elif option == "Forgot Password":
            recovery_email = st.text_input("Recovery Email")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")

            if st.button("Reset Password"):
                if new_password == confirm_new_password:
                    db = SessionLocal()
                    user = get_user_by_email(db, recovery_email)
                    if user:
                        user.hashed_password = generate_password_hash(new_password)
                        db.commit()
                        st.success("Password reset successfully!")
                        st.session_state['auth_action'] = "login"
                    else:
                        st.error("Invalid email address")
                else:
                    st.error("Passwords do not match")

if __name__ == "__main__":
    main()
