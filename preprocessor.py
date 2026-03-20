import re
import pandas as pd
def preprocessor(data):
    data = data.replace('\u202f', ' ').replace('\xa0', ' ')
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}\s+-\s+'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_message": messages, "Date": dates})
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y, %H:%M - ")
    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=["user_message"], inplace=True)
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month_name()
    df["day"] = df["Date"].dt.day
    df["hour"] = df["Date"].dt.hour
    df["minute"] = df["Date"].dt.minute
    return df
