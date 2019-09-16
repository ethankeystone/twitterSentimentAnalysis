# twitterSentimentAnalysis

-----
Description
-----
This program uses a Twitter API to scrape tweets off the internet and trains a model to evaluate the sentiment of those tweets.

-----
Requirements
----- 
**TensorFlow 1.4 or later**
> pip3 install tensorflow

**Tweepy**
> pip3 install tweepy

**pandas**
> pip3 install pandas

**numpy**
> pip3 install numpy

**sklearn**
> pip3 install sklearn

**keras**
> pip3 install keras


Running the program!
-----
Run the program using this format
python TwitterSentimentAnalysis.py --tweetName tweetNameString
                             --consumer_key consumer_keyString
                             --consumer_secret consumer_secretString
                             --access_token access_tokenString
                             --access_token_secret access_token_secretString

Where...
-----
tweetNameString = the wanted subject or person to be 

consumer_keyString, consumer_secretString, access_tokenString, and access_token_secretString are all the API strings given for registering for the Twitter API
