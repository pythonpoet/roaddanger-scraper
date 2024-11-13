import os, json
from database import *

path_to_json = 'test_data/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

db = ImagineAllTheData()

path_to_local_roaddanger_db="data/roaddanger_org_data_all_text.json"


        


def extract_roaddanger_article(json_text):
    try:
        coutry = get_country(json_text["latitude"], json_text["longitude"])
    except Exception as e:
        logError(f"Couldnt finde country for accident: {json_text['id']}")
        return
    for article in json_text["articles"]:

        # Clean summary because summary almost never contains different data than alltext
        if article["alltext"] == "":
            article["alltext"] = article["summary"]
    # Push article to supabase 
    try:
        db.pushArticle(headline=article["title"], alltext=article["alltext"], sitename=article["sitename"], url=article["url"], country=coutry, dateTime=article["publishedtime"], dataOrigin="roaddanger", articleID=article["id"])
        print(f"Uploaded articleID: {article['id']}")
    except Exception as e:
        print(f"Upload error in article: {article['id']}, err: {e} ")
    
# upload data from test data dir
def test_data():
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            extract_roaddanger_article(json_text)

def copy_roaddanger_article_to_supabase(path):
    print("Uploading local db to supabase")
    with open(path) as json_file:
        json_text = json.load(json_file)
        #loop over articles in file

        for article in json_text:

            extract_roaddanger_article(article)

copy_roaddanger_article_to_supabase(path_to_local_roaddanger_db)