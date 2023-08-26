from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df =  df[df['user']== selected_user]
    # fetch the number of messages   
    num_messages = df.shape[0]
     
    #fetch the number of words   
    words = []
    for message in df['messages']:
        words.extend(message.split())
    
    #fetch the number of media messages
    num_media_msg = df[df['messages'] == '<Media omitted>\n'].shape[0]
    
    # fetch number of links shared
    links = []
    for i in df['messages']:
        links.extend(extractor.find_urls(i))
    
    return num_messages,len(words),num_media_msg,len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    dat = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name','user':"% of Active"})
    return x,dat

def create_wordcloud(selected_user,df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
      
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep = ' '))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    
    words = []
    for i in temp['messages']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return_df.rename(columns = {0:'words',1:'repeatation'},inplace = True)
    return return_df

def emoji_helper(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
       
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']]) 
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.rename(columns = {0:'emoji',1:'repeatation'},inplace = True)
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year','month','month_num']).count()['messages'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(['dates']).count()['messages'].reset_index()
    
    return daily_timeline

def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    activity = df.pivot_table(index = 'day_name',columns = 'period',values = 'messages',aggfunc = 'count').fillna(0)
    return activity