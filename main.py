import twitter
import json
import datetime
from datetime import timedelta
import os
import io

# Create a credentials.json file in the project root and use it like this
#
# api = twitter.Api(consumer_key=[consumer key],
#                   consumer_secret=[consumer secret],
#                   access_token_key=[access token],
#                   access_token_secret=[access token secret])

with open('credentials.json') as json_file:
    data = json.load(json_file)

api = twitter.Api(consumer_key=data["api-key"],
                  consumer_secret=data["api-secret-key"],
                  access_token_key=data["access-token"],
                  access_token_secret=data["access-token-secret"])

since = str(datetime.date.today()-timedelta(1))
count = "1000"
nearAccra = "near%3A5.6231983%2C-0.18677313071441398%20within%3A20km&"


def query(keyword, since, maxcount):
    return api.GetSearch(raw_query="q="+keyword+"%20exclude%3Anativeretweets%20exclude%3Aretweets%20&result_type=recent&since="+since+"&count="+maxcount+"&tweet_mode=extended")


def queryLoc(keyword, since, maxcount, loc):
    return api.GetSearch(raw_query="q="+keyword+"%20&result_type=recent&since="+since+"&count="+maxcount+loc)


fname = "housingQuery.txt"

try:
    os.remove(fname)
except:
    print("File not found")

with io.open(fname, "w", encoding="utf-8") as f:
    housingQuery = query("housing", since, count)
    for res in housingQuery:
        f.write("\n---\n")
        f.write("Name: " + res.user.name)
        f.write("\n")
        f.write("Alias: " + res.user.screen_name)
        f.write("\n")
        f.write("Location: " + res.user.location)
        f.write("\n")
        f.write("Created at: " + res.user.created_at)
        f.write("\n")
        f.write(res.full_text)
    f.close()
