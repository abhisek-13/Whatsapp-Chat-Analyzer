import re
import pandas as pd

def preproces(data):
    # identifing the format of time (12 hr or 24 hr)
    pattern_1,pattern_2,frmt = format(data)
    
    message = re.split(pattern_1,data)[1:]
    
    dates = re.findall(pattern_2,data)
    
    
    #convert message_data type
    
    df = pd.DataFrame({'message':message,'date':dates})
    #convert date format
    df['date'] = pd.to_datetime(df['date'],format = frmt)
    
    
    # separating users and messages
    users = []
    messages = []
    for message in df['message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
        
    df['user'] = users
    df['messages'] = messages
    df.drop(columns = ['message'],inplace = True)
    
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['dates'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hr'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    df['hr'] = df['hr'].astype('int')
    df['minute'] = df['minute'].astype('int')
    
    period = []
    for hour in df[['day_name','hr']]['hr']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period
    return df

# identifing the format day/month or month/date
def format(data):
    pattern_x = '\s\d{1,2}:\d{2}\s'
    time_hr = re.findall(pattern_x,data)
    b = []
    l = 0
    for i in range(0,len(time_hr)):
        res = int(time_hr[i][1:].split(':')[0])
        b.append(res)
        res = 0
    for x in range(0,len(b)):
        if b[x] > 12:
            l+=1
            break
    if l == 0:
        pattern_1 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM,?:am|pm)\s-\s'
        pattern_2 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM,?:am|pm)'
    else:
        pattern_1 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        pattern_2 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}'
    
    message = re.split(pattern_1,data)[1:]
    
    dates = re.findall(pattern_2,data)
    # identifing the format day/month or month/date
    pattern = '/\d{1,2}/'
    r = re.findall(pattern,data)
    s = []
    t = []
    for i in range(0,len(r)):
        res = ''.join(filter(lambda i: i.isdigit(),r[i]))
        s.append(res)
        res = ''

    for i in range(0,len(s)):
        t.append(int(s[i]))
    y = 0
    for i in range(0,len(t)):
        if t[i] not in range(1,13):
            y+=1
        
    if y != 0:
        p = '%m/%d/%y, '
    else:
        p = '%d/%m/%y, '
        
    if pattern_2 == '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM,?:am|pm)':
        n = '%H:%M %p'
    else:
        n = '%H:%M'
    
    if p == '%m/%d/%y, ' and n == '%H:%M %p':
        p = '%m/%d/%y, %H:%M %p'
    elif p == '%m/%d/%y, ' and n == '%H:%M':
        p = '%m/%d/%y, %H:%M'
    elif p == '%d/%m/%y, ' and n == '%H:%M':
        p = '%d/%m/%y, %H:%M'
    else:
        p = '%d/%m/%y, %H:%M %p'
    return pattern_1,pattern_2,p