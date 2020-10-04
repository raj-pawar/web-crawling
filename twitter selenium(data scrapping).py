#chromedriver.exe file required to be in the same path as the code file for it to run
#File All.csv required for data
# Both files on same google drive link
'''Script to scrape tweets from a period of 2 months on a topic in this case, a movie with a relevant keyword in this case, the actor in the movie.
The scrapped tweets will be the tweets containing all the words of the topic and keyword in any order. '''
# Using Selenium to work around the infinite scrolling feature of twitter and scrape tweets from a particular time period which wasn't possible with the official
# data scrapping API of twitter i.e. tweepy and other libraries such as BeautifulSoup

# Importing required libraries
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

# Reading a file FROM LOCAL MACHINE to get data of the movie names, the name of the primary actor in it and the release dates.
# The movie names will be used as the topic and the actor name as a keyword and the dates to create a 2 month window before and after the release date of the movie
# for which tweets will be querried and scrapped.
# Strings containing movie names and actor names will be passed in the 'all of these words' field in the advanced search of the twitter web-page
# Querries can be manipulated accordingly to get desired tweets 
boia = pd.read_csv('C:\\Users\\Manju Pawar\\Desktop\\CP\\Data\\IMDB data\\Year wise popular movies\\All.csv')
tmpcol = list(boia['gtrendssearch'])
tmpcol = [tmpcol[i]+' movie' for i in range(len(tmpcol))]
boia['gtrendssearch'] = tmpcol
names = boia['gtrendssearch']
names = [(names[i]).lower() for i in range(len(names))]
names = [(names[i]).replace(' ','%20') for i in range(len(names))]
dates = boia['date']
since_dates = []
until_dates = []
search_urls = []
actors = []
searchwithactor_urls = []

# Common url
search_base_url = 'https://twitter.com/search?l=en&q='

# Creating since dates and until dates to pass to the advanced search page of twitter according to the release dates of the movies
for i in range(len(dates)):
    month = re.findall(r'-\d\d-', dates[i])
    month = ''.join(e for e in month[0] if e.isalnum())
    year = re.findall(r'\d\d\d\d', dates[i])[0]
    day = re.findall(r'-\d\d', dates[i])[1]
    day = ''.join(e for e in day if e.isalnum())
    
    
    sincemonth_dict = {'01':'12','02':'01','03':'02','04':'03','05':'04','06':'05',
                       '07':'06','08':'07','09':'08','10':'09','11':'10','12':'11'}
    untilmonth_dict = {'01':'02','02':'03','03':'04','04':'05','05':'06','06':'07',
                       '07':'08','08':'09','09':'10','10':'11','11':'12','12':'01'}

    since_month = sincemonth_dict[month]
    until_month = untilmonth_dict[month]
    
    if(month == '01'):
        since_year = str(int(year)-1)
    else:
        since_year = year

    if(month == '12'):
        until_year = str(int(year)+1)
    else:
        until_year = year

    since_date = since_year+'-'+since_month+'-'+day
    until_date = until_year+'-'+until_month+'-'+day

    since_dates.append(since_date)
    until_dates.append(until_date)

    search_name_url = names[i]+'%20'
    search_date_url = 'since%3A'+since_date+'%20until%3A'+until_date+'&src=typd'

    tmp = boia['cast'][i]
    tmp = tmp.split('Stars: ')
    tmp = tmp[1]

    actor = tmp.split(',')[0]
    actor = actor.lower() 
    actor = actor.replace(' ','%20')
    actors.append(actor)
    actor_url = actor+'%20'
    
    
    # Creating the search urls with only the movie names passed in the query
    search_url = search_base_url+search_name_url+search_date_url
    search_urls.append(search_url)
    
    # Creating the search urls with the movie names and the actor names passed in the query
    searchwithactor_url = search_base_url+search_name_url+actor_url+search_date_url
    searchwithactor_urls.append(searchwithactor_url)
    

browser = webdriver.Chrome()

# Loop to go through each url in search_urls where tweets for each movie will be querried, scrapped and stored in a csv file seperately
c = 0
for search_url in search_urls:
    print("Starting selenium for", names[c])
    
    browser.get(search_url)
    time.sleep(1)

    body = browser.find_element_by_tag_name('body')

    for _ in range(100):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    tweets = browser.find_elements_by_class_name('js-tweet-text')
    tweet_texts = []
    usernames = []
    handles = []
    dates = []
    replies = []
    retweets = []
    likes = []

    for i in range(len(tweets)):

        tweet_texts.append(tweets[i].text)

        userinfo_and_date = browser.find_elements_by_class_name('stream-item-header')[i]
        try:    
            username = userinfo_and_date.find_element_by_class_name('FullNameGroup').text
            usernames.append(username)
        except:
            usernames.append('NA')
            handles.append('NA')
            dates.append('NA')
            replies.append('NA')
            retweets.append('NA')
            likes.append('NA')
            continue 

        handle = userinfo_and_date.find_element_by_class_name('username').text
        handles.append(handle)

        date = userinfo_and_date.find_element_by_class_name('_timestamp').text
        dates.append(date)

        reply = browser.find_elements_by_class_name('js-actionReply')[i].text
        replies.append(reply)

        retweet =  browser.find_elements_by_class_name('js-actionRetweet')[i+i].text
        retweets.append(retweet)

        like = browser.find_elements_by_class_name('js-actionFavorite')[i+i].text
        likes.append(like)

##    # Scrapping the publically available proile info of the users whose tweets were collected by using their handles
##    print('Scrapping profile info')
##    common_url = 'https://twitter.com/'
##    var_urls = []
##    for i in range(len(tweets)):
##        var_urls.append(re.findall(r'[^@]\w+', handles[i]))
##    for i in range(len(tweets)):
##        var_urls[i] = ''.join(var_urls[i][0])
##    profile_urls = [common_url+var_urls[i] for i in range(len(tweets))]
##
##    users_descriptions = []
##    users_locations = []
##    users_no_of_tweets = []
##    users_followings = []
##    users_followers = []
##    users_likes = []
##
##    for url in profile_urls:
##        response = get(url)
##        html_soup = BeautifulSoup(response.text, 'html.parser')
##
##        user_description = html_soup.find('p', class_ = 'ProfileHeaderCard-bio u-dir').text
##        users_descriptions.append(user_description)
##
##        user_location = html_soup.find('span', class_ = 'ProfileHeaderCard-locationText u-dir').text
##        users_locations.append(user_location)
##
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--tweets is-active') is not None:
##            user_no_of_tweets = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--tweets is-active').text
##            users_no_of_tweets.append(user_no_of_tweets)
##        else:
##            users_no_of_tweets.append('NA')
##
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--following') is not None:
##            user_following = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--following').text
##            users_followings.append(user_following)
##        else:
##            users_followings.append('NA')
##            
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--followers') is not None:
##            user_followers = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--followers').text
##            users_followers.append(user_followers)
##        else:
##            users_followers.append('NA')
##            
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--favorites') is not None:
##            user_likes = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--favorites').text
##            users_likes.append(user_likes)
##        else:
##            users_likes.append('NA')
            

    df = pd.DataFrame({'Tweet': tweet_texts,
                       'Username': usernames,
                       'TwitterHandle': handles,
                       'TweetDate': dates,
                       'TweetNoOfReplies': replies,
                       'TweetNoOfRetweets': retweets,
                       'TweetNoOfLikes': likes,
                       })

    df.to_csv("C:\\Users\\Manju Pawar\\Desktop\\"+names[c]+".csv", index = False)
    print(c)
    print(names[c],"without actor Done")
    c = c + 1
    
## Running the same loop as above, this time with the name of the actor added to the query, to filter out the search results better
c = 0
for searchwithactor_url in searchwithactor_urls:
    print("Starting selenium for", names[c],"with actor")
    
    browser.get(searchwithactor_url)
    time.sleep(1)

    body = browser.find_element_by_tag_name('body')

    for _ in range(100):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    tweets = browser.find_elements_by_class_name('js-tweet-text')
    tweet_texts = []
    usernames = []
    handles = []
    dates = []
    replies = []
    retweets = []
    likes = []

    for i in range(len(tweets)):

        tweet_texts.append(tweets[i].text)

        userinfo_and_date = browser.find_elements_by_class_name('stream-item-header')[i]
            
        username = userinfo_and_date.find_element_by_class_name('FullNameGroup').text
        usernames.append(username)

        handle = userinfo_and_date.find_element_by_class_name('username').text
        handles.append(handle)

        date = userinfo_and_date.find_element_by_class_name('_timestamp').text
        dates.append(date)

        reply = browser.find_elements_by_class_name('js-actionReply')[i].text
        replies.append(reply)

        retweet =  browser.find_elements_by_class_name('js-actionRetweet')[i+i].text
        retweets.append(retweet)

        like = browser.find_elements_by_class_name('js-actionFavorite')[i+i].text
        likes.append(like)

##    # Scrapping the publically available proile info of the users whose tweets were collected by using their handles
##    print('Scrapping profile info')
##    common_url = 'https://twitter.com/'
##    var_urls = []
##    for i in range(len(tweets)):
##        var_urls.append(re.findall(r'[^@]\w+', handles[i]))
##    for i in range(len(tweets)):
##        var_urls[i] = ''.join(var_urls[i][0])
##    profile_urls = [common_url+var_urls[i] for i in range(len(tweets))]
##
##    users_descriptions = []
##    users_locations = []
##    users_no_of_tweets = []
##    users_followings = []
##    users_followers = []
##    users_likes = []
##
##    for url in profile_urls:
##        response = get(url)
##        html_soup = BeautifulSoup(response.text, 'html.parser')
##
##        user_description = html_soup.find('p', class_ = 'ProfileHeaderCard-bio u-dir').text
##        users_descriptions.append(user_description)
##
##        user_location = html_soup.find('span', class_ = 'ProfileHeaderCard-locationText u-dir').text
##        users_locations.append(user_location)
##
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--tweets is-active') is not None:
##            user_no_of_tweets = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--tweets is-active').text
##            users_no_of_tweets.append(user_no_of_tweets)
##        else:
##            users_no_of_tweets.append('NA')
##
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--following') is not None:
##            user_following = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--following').text
##            users_followings.append(user_following)
##        else:
##            users_followings.append('NA')
##            
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--followers') is not None:
##            user_followers = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--followers').text
##            users_followers.append(user_followers)
##        else:
##            users_followers.append('NA')
##            
##        if html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--favorites') is not None:
##            user_likes = html_soup.find('li', class_ = 'ProfileNav-item ProfileNav-item--favorites').text
##            users_likes.append(user_likes)
##        else:
##            users_likes.append('NA')
            

    df = pd.DataFrame({'Tweet': tweet_texts,
                       'Username': usernames,
                       'TwitterHandle': handles,
                       'TweetDate': dates,
                       'TweetNoOfReplies': replies,
                       'TweetNoOfRetweets': retweets,
                       'TweetNoOfLikes': likes,
                       })

    df.to_csv("C:\\Users\\Manju Pawar\\Desktop\\New folder (2)\\"+names[c]+actors[c]+".csv", index = False)
    print(c)
    print(names[c],"with actor Done")
    c = c + 1
