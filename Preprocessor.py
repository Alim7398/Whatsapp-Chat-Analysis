import re
import pandas as pd


def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_message": messages, "message_date": dates})
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%y, %H:%M - ")
    df.rename(columns={"message_date": "date"}, inplace=True)
    users = []
    messages = []

    for message in df["user_message"]:
        entry = re.split("([\w\W]+?):\s",message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group notification')
            messages.append(entry[0])

    df["user"] = users
    df["message"] = messages

    df.drop(columns=["user_message"], inplace=True)
    df["years"] = df["date"].dt.year
    df[ 'month_num' ] = df[ 'date' ].dt.month
    df["months"] = df["date"].dt.month_name()
    df[ 'only_date' ] = df[ 'date' ].dt.date
    df[ 'day_name' ] = df[ 'date' ].dt.day_name()
    df["day"] = df["date"].dt.day
    df["hours"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    periods = [ ]
    for hours in df[ [ 'day_name', 'hours' ] ][ 'hours' ]:
        if hours == 23:
            periods.append(str(hours) + "-" + str("00"))
        elif hours == 0:
            periods.append(str("00") + '-' + str(hours + 1))

        else:
            periods.append(str(hours) + '-' + str(hours + 1))

    df['periods'] = periods


    return df
