#NEEDED LIBRARIES
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid,GridOptionsBuilder
import pymongo
from datetime import datetime
import snscrape.modules.twitter as sntwitter

#CREATING PAGE SETUP
st.set_page_config(page_title="project")
selected=option_menu(menu_title="TWITTER SCRAPPING",
                     options=["HOME","SCRAP SEARCH","USER OPTIONS"],
                     icons=["house","search","download"],
                     menu_icon="twitter",
                     default_index=0,
                     orientation="horizontal")


#HOME PAGE
if selected=="HOME":
      st.info("""
                - Discover real-time insights and trends from the world of Twitter with  Twitter Scraping Project.
                - Uncover valuable data, analyze user sentiments, track hashtags, and monitor conversations in a user-friendly interface.
                - Stay up-to-date with the latest happenings, harness the power of social media, and gain valuable insights with Twitter Scraping Project.""")

#SCRAP SEARCH
tweets=[]
if selected=="SCRAP SEARCH":
      st.subheader("ENTER THE FOLLOWING TO SCRAP")
      with st.form("ENTER THE DETAILS"):
             keyword=st.text_input("ENTER THE KEYWORD TO SEARCH")
             count = st.number_input("ENTER NO OF TWEETS TO SCRAP", min_value=1, max_value=100, value=10, step=1, format=None, key=None)
             stdate=st.date_input("ENTER START DATE ")
             enddate=st.date_input("ENTER END DATE ")
             # Convert date input to datetime format
             start_datetime = datetime(stdate.year, stdate.month, stdate.day, 0, 0, 0)
             end_datetime = datetime(enddate.year, enddate.month, enddate.day, 23, 59, 59)

             scrbutton=st.form_submit_button("SCRAP")
             if scrbutton:
                  
                  for i, tweet in enumerate(sntwitter.TwitterUserScraper(f'{keyword} lang:en since:{start_datetime} until:{end_datetime}').get_items()):
                            if i+1 == count:
                                   break
                            tweets.append([
                                           tweet.date,
                                           tweet.id,
                                           tweet.url,
                                           tweet.rawContent,
                                           tweet.user.username,
                                           tweet.replyCount,
                                           tweet.retweetCount,
                                           tweet.likeCount,
                                           tweet.lang,
                                           tweet.source
                                           ])
                  st.success("tweets scrapped")

df=pd.DataFrame(tweets,columns=["datetime","userid","url","content","username","replycount","retweetcount","like count","language","source"])
csvformat=df.to_csv().encode('utf-8')#converting to csv format
jsonformat=df.to_json(orient='index')#converting to json format


if selected=="USER OPTIONS":
    
    if  df.empty:
           choosen=st.selectbox("choose the one you need",["DOWNLOAD","UPLOAD TO DB","VIEW THE SCRAPED DATA"], index=0)
           if choosen=="DOWNLOAD":
               col1,col2=st.columns(2)
               #download buttons
               with col1:
                       st.download_button(label= "Download data as CSV",
                                          data= csvformat,
                                          file_name= 'scraped_tweets.csv',
                                          mime= 'text/csv'
                                          )
               with col2:
                      st.download_button(label= "Download data as JSON",
                                         data= jsonformat,
                                         file_name= 'scraped_tweets.json',
                                         mime= 'text/csv'
                                         )
          #to show scrapped data in table format
           if choosen=="VIEW THE SCRAPED DATA":
               st.write("Scrapped data is")
               AgGrid(df)
          #to upload the scrapped data to mongodb database
           if choosen=="UPLOAD TO DB":
               client = pymongo.MongoClient("mongodb://localhost:27017")
               db = client["mydatabase"]
               data_dict = df.to_dict("records")
               collection = db["mycollection"]
               if not data_dict:# Check if the list is not empty
                      if st.button("UPLOAD TO DB", use_container_width=False):
                           collection.insert_many(data_dict)
               else:
                      st.write("No documents to insert. The data list is empty.")
               client.close()



               


               
    #else:
        #st.warning("please scrap the tweets")
    
    










    
                    
