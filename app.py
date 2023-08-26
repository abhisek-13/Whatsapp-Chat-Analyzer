import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns
import re

st.set_page_config(page_title = 'Whatsapp Chat Analyzer',page_icon = ':tada:')
with st.container():
    st.header('Hi, I am Abhisek :wave:')
    st.title('Whatsapp Chat Analyzer')
    st.write('Visualize your chats from words to insights.')
    st.write('---')

st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('Choose your chat file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess.preproces(data)
    
    
# fetch unique users
    p = 0
    b = 0
    user_list = df['user'].unique().tolist()
    for i in range(0,len(user_list)):
        if user_list[i] == 'group_notification':
            p+=1
            break
        
    if p == 1:
        user_list.remove('group_notification')
    else:
        p = 0
        
    for i in user_list:
            var = i.split()
            if len(var) <= 4:
                var = ''
            else:
                user_list.remove(i)
    for i in user_list:
        if len(i) > 40:
            user_list.remove(i)
            
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox('Select User Name',user_list)
    
    if st.sidebar.button('Click Here'):
        
        num_messages,words,num_media,links = helper.fetch_stats(selected_user,df)
        st.title('Whatsapp Statistics')
        st.write('##')
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
            
        with col2:
            st.header('Total Words')
            st.title(words)
            
        with col3:
            st.header('Media Shared')
            st.title(num_media)
        with col4:
            st.header('Link Shared')
            st.title(links)
        
        # timeline of users(monthly)
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['dates'],daily_timeline['messages'],color = 'purple')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        # most active day and month
        st.title('Weekly Activity')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Active Day')
            busy_day = helper.week_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Active Month')
            busy_month = helper.month_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'green')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        
        # activity heatmap
        st.title('Active Time Period')
        st.subheader('More Brighter the color, More Active at that time period.')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        # finding the busiest person in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_dat = helper.most_busy_user(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_dat)   
            
        
        # used words
        st.title('used words')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # most common words
        st.title('Most Common Words')
        return_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(return_df['words'],return_df['repeatation'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        # emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Used")
        s1,s2 = st.columns(2)
        
        with s1:
            st.dataframe(emoji_df.head(10))
        with s2:
            fig,ax = plt.subplots()
            ax.bar(emoji_df['emoji'].head(),emoji_df['repeatation'].head(),color = 'orange')
            #plt.xticks(rotation = 'vertical')
            st.pyplot(fig)