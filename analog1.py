#!/usr/bin/env python
# coding: utf-8

# In[8]:


from pyfirmata import Arduino, util
import chestnut.graph as graph
import tweepy
import time
from tweepy import OAuthHandler
from sense_hat import SenseHat

board = Arduino('/dev/ttyACM0')
pin = board.get_pin('a:0:i')
buzz = board.get_pin('d:9:o')
redlight = board.get_pin('d:4:o')
yellowlight = board.get_pin('d:3:o')
greenlight = board.get_pin('d:2:o')
sense = SenseHat()

it = util.Iterator(board)
it.start()
consumer_key = "Q1tK6VHSOywwIareectfHu4js"
consumer_secret = "cDo5FgeppEJPGUZgnQB5Y8IUwcnQWXbbbVJM8mR9OrGbm2enKq"
access_token = "1385538711065083904-ZPtvthvHmEYXK9PKRz5tV9hXlnFeoI"
access_token_secret = "E3GvSSROE0Px7CTY26nVY9b1oFHurVDSK5XC6wRKiYONJ"

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)
last_tweet_time = time.time()

analog_value = pin.read()
while analog_value is None:
    analog_value = pin.read()
line = graph.Line(['Data 1'])
while True:
    current_time = time.time()
    analog_value = pin.read()
    if analog_value <= 0.32:
        redlight.write(1)
        yellowlight.write(0)
        greenlight.write(0)
        sense.clear(255, 0, 0) 
        print("Red Weather warning: It is below freezing")
        buzz.write(1)
    elif 0.32 < analog_value <= 0.50:
        redlight.write(0)
        yellowlight.write(1)
        greenlight.write(0)
        sense.clear(255, 255, 0)  
        print("Yellow Weather Warning: It is below 10 degrees Celsius")
        buzz.write(0)
    elif 0.50 < analog_value <= 0.95:
        redlight.write(0)
        yellowlight.write(0)
        greenlight.write(1)
        sense.clear(0, 255, 0)
        print("It is mild")
        buzz.write(0)
    else:
        redlight.write(0)
        yellowlight.write(0)
        greenlight.write(0)
        sense.clear(0, 0, 0)
        print("Off")
        buzz.write(0) 
    if current_time - last_tweet_time >= 30:
    
        response = client.create_tweet(text="The temperature is %d%% Fahrenheit" % (analog_value * 100))
        print(f"https://twitter.com/user/status/{response.data['id']}")

    
        last_tweet_time = current_time

    print(analog_value)
    line.update([analog_value])
    time.sleep(1)


# In[ ]:





# In[ ]:





# In[ ]:




