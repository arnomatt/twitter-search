import twitter
import json
import datetime
from datetime import timedelta
import os
import io

# CONFIGURATION
# Days to go back in search
DAYS = 7
# Max number of retrieved tweets
COUNT = "2000"
# CONFIGURATION END

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

since = str(datetime.date.today()-timedelta(DAYS))
count = COUNT
# Accra geoloc
loc = "near%3A5.6231983%2C-0.18677313071441398%20within%3A20km&"
root_path = "results/"


def setupQuery(filename, keyword, loc=""):
    def query():
        return api.GetSearch(raw_query="q="+keyword+"%20exclude%3Anativeretweets%20exclude%3Aretweets%20&result_type=recent&since="+since+"&count="+count+"&tweet_mode=extended&"+loc)

    fname = root_path+filename

    try:
        os.remove(fname)
    except:
        print("File not found")

    with io.open(fname, "w", encoding="utf-8") as f:
        queryResults = query()
        for res in queryResults:
            f.write("\n---\n")
            f.write("Name: " + res.user.name)
            f.write("\n")
            f.write("Alias: " + res.user.screen_name)
            f.write("\n")
            f.write("Location: " + res.user.location)
            f.write("\n")
            f.write("Created at: " + res.created_at)
            f.write("\n")
            f.write(res.full_text)
        f.close()


setupQuery("housing_WithAccraGeoLoc.txt", "housing", loc)
setupQuery("housing_Accra.txt", "housing accra")
setupQuery("housing_Ghana.txt", "housing ghana")
