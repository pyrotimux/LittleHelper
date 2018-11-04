import urllib2
import json


"""
Given a csv file with titles, retrieve the fields from omdbapi.
Args:
    titles_csv (str): csv with titles.
    api_key (str): omdbapi key for requests.
"""
def add_fields_to_title(titles_csv, api_key):
    with open(titles_csv) as in_file: # read the tiltes
        titles = in_file.read().split("\n")
        for title in titles: # on every title we request info then write to csv
            item = json.loads(urllib2.urlopen("https://www.omdbapi.com/?t="+urllib2.quote(title)+"&plot=full&apikey="+api_key).read())

            if 'Response' in item  and item['Response'] == 'True':
                try:
                    with open("cacheddata2.csv", "a") as out_file:
                        out_file.write(item["Title"] + "||||" + item["Plot"] + "||||" + item["Year"] 
                        + "||||" + item["Type"] + "||||" + item["Rated"] + "||||" + item["Genre"] + "\n")
                except:
                    pass # we are going to ignore the errors that occur due to non english characters


add_fields_to_title("tv.csv", "")
add_fields_to_title("movies.csv", "")