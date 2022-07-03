from pattern.web import Twitter, Google
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import pandas as pd
import discord

##text = input("Enter Name of NFT Project To Analyze: ")

def get_sentiment(text):
    tweets = []
    twitter = Twitter(language='en')
    for tweets_list in twitter.search(  text + '-"#'+text+'"', cached=False, count=10000):
        tweets.append(tweets_list.text)

    tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
    tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

    analyzer = SentimentIntensityAnalyzer()

    new_words = {
        'wgmi': 4,
        'ngmi': -4,
        '🔥' : 4,
        'hacked' : -1,
        'rug': -2,
        'was rugged': -4
    }
    analyzer.lexicon.update(new_words)


    tweet_score = analyzer.polarity_scores((tweets))
    tw_df = pd.DataFrame(tweet_score, index=[0])

    tweet_mean = (tw_df['compound'].mean())
    if(tweet_mean == 0):
        return "Not Valid Search"
    return tweet_mean

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!search'):
        text = message.content[message.content.index(' ')+1:]
        await message.channel.send(get_sentiment(text))
    
    if message.content.startswith('!help'):
        await message.channel.send("> `Command`: `!search <NFT Project Name>`")

client.run('OTkzMjk2MTE2ODczNDI5MTEy.GJkbG6.IUEKvS0axE7tU9FrubtFwasO6hicD1lKwOoU-A')