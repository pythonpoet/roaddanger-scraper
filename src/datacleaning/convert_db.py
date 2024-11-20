# 
# This file is for converting roaddanger.org/export database to a sqlite db
# 
import os, json
from sqlite_db import *

path_to_json = 'data/new_roaddanger_data.json'
path_to_database = "david_data.db"

def logError(log_entry, logfile_path="logfile.txt"):
    with open(logfile_path, "a") as logfile:
        logfile.write(log_entry + "\n")

      
def copy_routine():
    data = open_roaddanger_db(path_to_json)

    for crash_data in data["crashes"]:
        try:
            # Connect to SQLite database
            connection = sqlite3.connect(path_to_database)
            # Insert crash table
            create_crash_table(connection, crash_data)
            # Insert person table
            for person in crash_data["persons"]:
                create_person_table(connection, person, crash_id=crash_data["id"])
            
            # Insert articles
            for article in crash_data["articles"]:

                # Clean summary because summary almost never contains different data than alltext
                if article["alltext"] == "":
                    article["alltext"] = article["summary"]

                cleaned_url = roaddanger_clean_url(article["url"])

                pushArticle(
                    connection,
                    headline=article["title"],
                    alltext=article["alltext"], 
                    sitename=article["sitename"], 
                    url=cleaned_url,
                    # Use countryid from crash table
                    country=crash_data["countryid"], 
                    dateTime=article["publishedtime"], 
                    dataOrigin="roaddanger", 
                    articleID=article["id"])
                print(f"Uploaded articleID: {article['id']}")

            
        except Exception as e:
            logError(f"Error for crash: {crash_data['id']}, msg: {e}")
        

        finally:    
            connection.close()

def open_roaddanger_db(path):
    with open(path) as json_file:
        return json.load(json_file)

if __name__ == "__main__":
    copy_routine()