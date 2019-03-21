import tweepy
from collections import defaultdict
import operator
import numpy as np
import random
from pyspark import SparkConf, SparkContext
#override tweepy.StreamListener to add logic to on_status

APP_NAME = "INF553"


class MyStreamListener(tweepy.StreamListener):

    # def __init__(self):
    #     self.store = []
    #     self.message_count = 0

    def on_status(self, status):
        global container
        global tags
        global count

        def tag_stat(queue,number):
            d = defaultdict(int)
            for elements in queue:
                for element in elements:
                    d[element] += 1
            sorted_x = sorted(d.items(), key=operator.itemgetter(1))
            return sorted_x[::-1][:number]

        cur_words = status.entities.get('hashtags')
        cur_text = status.text
        count += 1
        hots_tag = []
        for word in cur_words:
            hots_tag.append(word['text'])
        tags.append(hots_tag)

        container.append(cur_text)
        if len(container) == 101:
            if random.random() < 100/101.0:
                index = range(100)
                random.shuffle(index)
                pick = index[0]
                container.pop(pick)
                tags.pop(pick)
            else:
                container.pop()
                tags.pop()

        if len(container) == 100:
            print ('The number of the twitter from beginning: %s' % count)
            print ('Top 5 hot hashtags:')
            for i in tag_stat(tags,5):
                print ('%s: %s' % (i[0].encode('utf-8'),i[1]))
            print ('The average length of the twitter is: %s' % np.mean([len(i) for i in container]))


def main(sc):
    consumer_key="pd0XhiTlsmbgXPqwpX2mhRP5E"
    consumer_secret="eijLvoc0NliKSN9qbyFvLwgLzcZ39UlZCRwNxaYJfSCUoDKUBg"
    access_key = "901373171646873600-w3j1JImVYu7BUtQNCSpdHpDiv3tMjIl"
    access_secret = "WHrN0YiJiV3fthivKGzoe2FtVomatOeXjMVUpWaCgWKQ4"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    myStream = tweepy.streaming.Stream(auth, MyStreamListener())
    myStream.filter(track=['#'])


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    sc.setLogLevel(logLevel ="OFF")
    container = []
    tags = []
    count = 0
    # Execute Main functionality
    main(sc)