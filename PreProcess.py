import string
import pandas as pd
from spellchecker import SpellChecker
from langdetect import detect
def proccessTweets(tweets):
    retweet = []

    for tweet in tweets:
        if(str(tweet)[0:4] == 'b\"RT' or str(tweet)[0:4] == 'b\'RT'):
            retweet.append(True)
        else:
            retweet.append(False)

    retweet_person = []

    for i in range(len(retweet)):
        if(retweet[i]):
            bottom = 5
            top = 0
            for j in range(5,len(tweets[i])):
                if(str(tweets[i])[j] == ' '):
                    top = j - 1
                    break
            retweet_person.append(str(tweets[i])[bottom:top + 1])
        else:
            retweet_person.append('None')


    cleaned_tweets = []

    for text in tweets:
        cleaned_tweets.append(text)

    for i in range(len(tweets)):

        cleaned_tweets[i] = (processTweet(cleaned_tweets[i]))


    df = pd.DataFrame({'Text' : cleaned_tweets, 'Retweet' : retweet,'Retweeted Person' : retweet_person})

    return(df)
def processTweet(tweet):
    if(tweet[0] == 'b'):
        if(tweet[0:4] == 'b\'RT' or tweet[0:4] == 'b\"RT'):
            tweet = tweet[4:len(tweet)]
        elif(tweet[0:2] == 'b\''):
            tweet = tweet[2:len(tweet)]

    tweet = removeLink(tweet)

    tweet = removeRandomBitCode(tweet)

    tweet = removePunctuation(tweet)

    tweet = removeStart(tweet)

    #   tweet = fixSpelling(tweet)
    return(tweet)
def removeStart(tweet):
    if(tweet[0] == 'b'):
        if(tweet[0:3] == 'bRT'):
            tweet = tweet[4:len(tweet)]
        else:
            tweet = tweet[1:len(tweet)]

    return tweet
def removeLink(tweet):
    returnString = str(tweet)
    while((returnString).find('https') != -1):
        bottom = (returnString).find('https')

        top = 0

        for i in range(bottom,len(returnString)):
            if(returnString[i] == ' '):
                top = i
                break
        if(top == 0):
            top = len(returnString)

        returnString = returnString[0:bottom] + returnString[top:len(returnString)]

    return(returnString)

def removeRandomBitCode(retweet):
    tweet = str(retweet)
    for i in range(len(tweet)):
        if(i >= len(tweet)):
            break
        if(tweet[i] == '\\'):
            bottom = i
            top = 0

            if(tweet[i:i+2] != '\\n'):
                for j in range(i,len(tweet)):
                    if(tweet[j] == ' '):
                        top = j
                        break
                if(top == 0):
                    top = len(tweet)

                tweet = tweet[0:bottom] + tweet[top:len(tweet)]
    return(tweet)

def removePunctuation(tweet):

    for char in string.punctuation:
        tweet = str(tweet).replace(char,'')
    return(tweet)


def fixSpelling(tweet):
    spell = SpellChecker()
    returnTweet = ''
    for word in tweet.split():
        returnTweet = returnTweet + ' ' + (spell.correction(word))
    return(returnTweet)

def isEnglish(tweet):
    if(detect(str(tweet)) == 'en'):
        return True
    return False
