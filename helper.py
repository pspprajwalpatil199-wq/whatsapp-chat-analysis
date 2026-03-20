import re

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # Total messages
    num_messages = df.shape[0]

    # Total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Media messages
    media_messages = df[df['message'].str.contains('omitted', case=False, na=False)].shape[0]

    # Links
    links = []
    for message in df['message']:
        links.extend(re.findall(r'https?://\S+', message))

    return num_messages, len(words), media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()

    # percentage
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['name', 'percent']

    return x, df_percent

from collections import Counter

def most_common_words(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    words = []

    for message in df['message']:
        words.extend(message.lower().split())

    # ❌ remove unwanted words
    stop_words = ['the','is','and','to','a','in','of','for','on','at','with','this','that','it','i','you']

    filtered_words = [word for word in words if word not in stop_words]

    common_words = Counter(filtered_words).most_common(10)

    return common_words
