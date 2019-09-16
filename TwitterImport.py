import tweepy
import csv
import datetime
import CSVHandler
import pandas as pd
import PreProcess
def generateDailyTwitterData(search, amount, path, consumer_key, consumer_secret, access_token, access_token_secret):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)


    stringName = search

    query = search
    max_tweets = amount
    print("Searching Through Tweets")
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    print('finished searching through twitter')


    date = datetime.datetime.today()
    dateString = (str(date.month) + '-' + str(date.day) + '-' + str(date.year))

    text = []
    removedTweets = []
    count = 0

    for a in searched_tweets:
        count += 1
        if(not PreProcess.isEnglish(a.text.encode("utf-8"))):
            removedTweets.append(searched_tweets[count])
            del searched_tweets[count]
    for a in searched_tweets:
            text.append(a.text.encode("utf-8"))

    id = []

    for a in searched_tweets:
        id.append(a.id_str)

    dateCreated = []

    for a in searched_tweets:
        dateCreated.append(a.created_at)

    user = []

    for a in searched_tweets:
        user.append(a.user.name)

    screen_name = []

    for a in searched_tweets:
        screen_name.append(a.user.screen_name)

    location = []

    for a in searched_tweets:
        location.append(a.user.location)

    cleaned_text = []

    df2 = PreProcess.proccessTweets(text)

    cleaned_text = df2.loc[:,'Text']

    retweet = df2.loc[:,"Retweet"]

    retweet_person = df2.loc[:,'Retweeted Person']

    data = {'ID' : id, 'Text' : text, 'Date Created' : dateCreated,
     'Username' : user, "Twitter Screen Name" : screen_name, "Location" : location,
     "Cleaned Text" : cleaned_text, 'Retweet' : retweet, 'Retweeted Person' : retweet_person}
    df = pd.DataFrame(data)
    print('save to file')
    dfDeleted = pd.DataFrame({'Deleted Tweets' : removedTweets})
    dfDeleted.to_csv(path + "deleted tweets.csv")
    df.to_csv(path + stringName + '- ' + str(amount)+ ' Twitter Tweets-'+ dateString + '.csv')
    #CSVHandler.writeToNewCSVFile(path + stringName + '-Twitter Tweets-'+ dateString + '.csv'path + stringName + '-Twitter Tweets-'+ dateString + '.csv', outputArray2, True)

    return(df)
