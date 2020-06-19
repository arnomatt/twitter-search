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
# Geocode for searching around Accra in a range of 20km
GEOCODE = "geocode%3A5.550000%2C-0.020000%2C20km%20"
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


def setupQuery(filename, keyword, geocode=""):
    since = str(datetime.date.today()-timedelta(DAYS))

    def query():
        return api.GetSearch(raw_query="q="+keyword+"%20"+geocode+"%20exclude%3Anativeretweets%20exclude%3Aretweets%20&result_type=recent&since="+since+"&count="+COUNT+"&tweet_mode=extended")

    fname = "results/" + filename + "_since_" + since + ".txt"

    try:
        os.remove(fname)
    except:
        print("File not found, creating a new one")

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


setupQuery("housing_WithAccraGeoLoc", "housing", GEOCODE)
setupQuery("housing_Accra", "housing accra")
setupQuery("housing_Ghana", "housing ghana")
