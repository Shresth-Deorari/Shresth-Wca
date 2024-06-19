from urlextract import URLExtract
from collections import Counter
import emoji
import pandas as pd
from wordcloud import WordCloud
get_urls = URLExtract()

def stats(selected_user, df):
    #Chagne df according to User
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #Find total messages
    total_messages = df.shape[0]

    #Find total words
    words = [word for message in df['message'] if isinstance(message, str) for word in message.split()]

    #Find the total media count
    media_count = df[df['message'] == "<Media omitted>\n"].shape[0]

    #find the total number of urls
    urls = []
    for i in df['message']:
        urls.extend(get_urls.find_urls(i))

    #Return Stats of the user
    return total_messages, len(words),media_count,len(urls)

def Most_Active_Users(df):
    most_active = []
    most_active = df['user'].value_counts().head()
    df = (round(((df['user'].value_counts()/df.shape[0])*100),2).reset_index().rename(columns = {'user':'name','count':'percentage'}))
    return most_active,df

def Create_Word_Cloud(selected_user, df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    # Remove specific messages and user 'group_notification'
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']

    # Read stop words from file
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())

    # Function to filter out stop words from each message
    def remove_stop_words(message):
        if isinstance(message, str):
            return ' '.join([word.lower() for word in message.split() if word.lower() not in stop_words])
        else:
            return ''

    # Apply stop word removal to each message
    df['clean_message'] = df['message'].apply(remove_stop_words)

    # Concatenate all cleaned messages into a single string
    text = " ".join(df['clean_message'].dropna())

    # Generate the WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    wc_img = wc.generate(text).to_image()  # Convert WordCloud to image

    return wc_img

def most_common_words(selected_user,df) :
    if(selected_user!='Overall'):
        df = df[df['user']==selected_user]
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    words = []
    for message in df['message']:
        # Split message into words, convert to lowercase, and filter out stop words
        message_words = [word.lower() for word in message.split() if word.lower() not in stop_words]
        words.extend(message_words)

    # Create a DataFrame of the most common words
    word_counts = Counter(words).most_common(20)
    common_df = pd.DataFrame(word_counts, columns=['Word', 'Frequency'])
    return common_df

def Emoji_Analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_counter = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counter.most_common(20), columns=['emoji', 'count'])

    return emoji_df
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Group by year and month, count the messages
    timedf = df.groupby(['year', 'month']).count()['message'].reset_index()

    # Add a numerical month column for sorting
    timedf['month_num'] = timedf['month'].map(month_mapping)
    timedf = timedf.sort_values(by=['year', 'month_num'])

    # Create the time list
    timedf['time'] = timedf.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timedf

