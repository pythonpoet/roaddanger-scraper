import os
import json
import pandas as pd
from datacleaning.sqlite_db import *
def get_data():
    connection = sqlite3.connect("C:/Users/david/OneDrive/Documents/Studium/UvA/Connections/roaddanger.org/roaddanger scraper/src/datacleaning/david_data.db")
    data= get_table(connection, "articles")
    df = pd.DataFrame(data)
    df = df.rename(columns={'id': 'articleid'})
    df["articleid"] = df["articleid"].astype(str)
    return df
def get_label_index():
    # Open file
    path_to_json = 'C:/Users/david/OneDrive/Documents/Studium/UvA/Connections/roaddanger.org/roaddanger scraper/data/roaddanger_org_research_data.json/roaddanger_org_research_data.json'
    
    with open(path_to_json) as json_file:
        data = json.load(json_file)
    
    # Check if the dataset is correct
    if not len(data["answers"]) == 10701:
        raise Exception("Wrong dataset")

    # Process data
    data = data["answers"]
    data = [item for item in data if item["questionid"] != 16]

    if not len(data) == 7422:
        raise Exception("Data specified is malformed")

    dehumanising_dic = {}
    df = pd.DataFrame(data)
    articles = df["articleid"].unique()
    
    for article in articles:
        dehumanising_dic[article] = df[df["articleid"] == article]
    
    if not len(dehumanising_dic) == 3731:
        raise Exception("Data specified is malformed 2")

    keys_to_remove = []
    for key, value in dehumanising_dic.items():
        q = value['questionid']
        if not (q >= 10).all():
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        dehumanising_dic.pop(key, None)

    if not len(dehumanising_dic) == 3691:
        raise Exception("Expected different data")

    new_dict = {}
    for key, value in dehumanising_dic.items():
        s = value["answer"].replace(2, 0)
        s = s.replace(1, 1)
        new_dict[key] = s.sum()
    df = pd.DataFrame(list(new_dict.items()), columns=['articleid', 'dehumanisation_score'])
    df["articleid"] = df["articleid"].astype(str)
    return df
def get_labled_data():
    return pd.merge(get_data(), get_label_index())
def translate_text(text, src_lang='auto', dest_lang='en'):
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(source=src_lang, target=dest_lang)

    # Translate the text
    try:
        return translator.translate(text)

    except Exception as e:
        return f"Translation failed: {e}"
if __name__ == "__main__":
    data = get_labled_data()
    print(data.head())
    print(translate_text(str(data["headline"][0])))