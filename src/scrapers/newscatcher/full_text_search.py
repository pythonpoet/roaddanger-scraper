from langdetect import detect
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.analysis import SimpleAnalyzer, StemmingAnalyzer
from whoosh.filedb.filestore import RamStorage
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, NgramFilter, CharsetFilter
from whoosh.support.charset import accent_map
from io import BytesIO
# Create an in-memory index
from whoosh import index
import os
import sys
import json


def GermanWordAnalyzer():
    """Creates an analyzer that handles compound words for German."""
    tokenizer = RegexTokenizer()  # Basic regex-based tokenizer
    # Chain the tokenizer with lowercase and stop-word filters
    return (tokenizer |
            LowercaseFilter() |
            NgramFilter(minsize=3, maxsize=15) | # Create n-grams for partial matching --> important for german for composit words
            CharsetFilter(accent_map) |  # Normalize special characters (e.g., umlauts)
            StopFilter(lang="de"))

def get_analyzer(text):
    lang = detect(text)
    #return SimpleAnalyzer()
    if lang == "de":
        return GermanWordAnalyzer()
        #return StemmingAnalyzer("german")
    elif lang == "en":
        return StemmingAnalyzer("english")
    elif lang == "fr":
        return StemmingAnalyzer("french")
    else:
        return SimpleAnalyzer()  # Default fallback

def search_in_text(query: str, text:str):
    # Define schema for full-text indexing
    schema = Schema(content=TEXT(stored=True, analyzer=get_analyzer(text)))

    # Create an in-memory storage
    ram_storage = RamStorage()  # In-memory storage
    ix = ram_storage.create_index(schema)  # Create an in-memory index
    writer = ix.writer()
    writer.add_document(content=text)
    writer.commit()

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(query)
        if results:
            #print("The text matches the expression!")
            return True
        else:
            print("The text does not match the expression.")
            return False
def load_from_json(filename):
    """Loads a dictionary from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def test_data():
    query = "Unfall AND Verkehr"
    title = "Frage des Tages: Bereit für den Wintereinbruch? +++ Zwei Thurgauer räumen bei Geografie-Olympiade ab +++ Kantonspolizei Thurgau: Kampagne gegen Gewalt an Frauen"
    exerpt = "Was passiert gerade im Thurgau? In unserem Ticker finden Sie aktuelle News aus dem Kanton und seinen Gemeinden."
    text = "Frage des Tages: Sind die Winterpneus am Fahrzeug schon montiert?\nDie Meteorologen warnen, dass am Mittwoch eine Kaltfront über den Thurgau zieht, die kräftigen Regen und Schnee bis auf rund 400 Meter über Meer bringen soll. Deshalb ist es höchste Zeit, sich Gedanken über die Winterpneus zu machen, sofern das nicht schon längst passiert ist. (red)\n15:07 Uhr Dienstag, 19. November\nZwei Bronzemedaillen für Landschlacht und Amriswil\nFlüsse und Hauptstädte auswendig lernen? Darum geht es bei der Geografie-Olympiade nicht."

    title2 = "Unfall mit drei Autos auf der Fulachstrasse – Strasse wieder frei"
    expert2 = "Auf der Fulachstrasse kam es am Donnerstagmorgen zu einem Unfall. Die Strasse war zeitweise gesperrt – mittlerweile rollt der Verkehr wieder."
    text2 = "Die Fulachstrasse kam es am Donnerstagmorgen gegen 6.40 Uhr im Bereich zwischen Schönbrücke bis zur Kreuzung Bachstrasse zu einem Verkehrsunfall mit drei Fahrzeugen. Wie die Polizei mitteilt, kam es aus bisher unbekannten Gründen zu einer Frontalkollision zwischen zwei Autos. Ein nachfolgender dritter Wagen konnte nicht mehr rechtzeitig bremsen und prallte ebenfalls mit beiden anderen Unfallfahrzeugen zusammen.\nBei dem Unfall wurden zwei Personen verletzt, die Schwere der Verletzungen sind bislang nicht bekannt."
    #results = search_in_text(query=query,text=title + exerpt)
    #results = search_in_text(query, text=title2 + expert2 + text2)
    
    articles = load_from_json("nc_articles.json")
    i = 0 
    for article in articles[40:]:
    #a = Article(article["link"])
    #a.download()
    #a.parse()
        result = search_in_text(query, article["title"]  + article["summary"])
        if not result:
            
            print(f"article_id: {article['_id']}, Matches: {result} ")
            i += 1
        else:
            print(f"article_id: {article['_id']}, Matches: {result} ")
    print(i, ": Articles have been filtered")
if __name__ == "__main__":
    test_data()
    sys.exit(0)
    query = "Verkehr AND Unfall"
    text = "Ein Verkehrsunfall ereignete sich in Deutschland."

    matches = search_in_text(query, text)
    print("Matches:", matches)
    query = "Unfall AND Verkehr"
    title = "Frage des Tages: Bereit für den Wintereinbruch? +++ Zwei Thurgauer räumen bei Geografie-Olympiade ab +++ Kantonspolizei Thurgau: Kampagne gegen Gewalt an Frauen"
    exerpt = "Was passiert gerade im Thurgau? In unserem Ticker finden Sie aktuelle News aus dem Kanton und seinen Gemeinden."
    text = "Frage des Tages: Sind die Winterpneus am Fahrzeug schon montiert?\nDie Meteorologen warnen, dass am Mittwoch eine Kaltfront über den Thurgau zieht, die kräftigen Regen und Schnee bis auf rund 400 Meter über Meer bringen soll. Deshalb ist es höchste Zeit, sich Gedanken über die Winterpneus zu machen, sofern das nicht schon längst passiert ist. (red)\n15:07 Uhr Dienstag, 19. November\nZwei Bronzemedaillen für Landschlacht und Amriswil\nFlüsse und Hauptstädte auswendig lernen? Darum geht es bei der Geografie-Olympiade nicht."

    title2 = "Unfall mit drei Autos auf der Fulachstrasse – Strasse wieder frei"
    expert2 = "Auf der Fulachstrasse kam es am Donnerstagmorgen zu einem Unfall. Die Strasse war zeitweise gesperrt – mittlerweile rollt der Verkehr wieder."
    text2 = "Die Fulachstrasse kam es am Donnerstagmorgen gegen 6.40 Uhr im Bereich zwischen Schönbrücke bis zur Kreuzung Bachstrasse zu einem Verkehrsunfall mit drei Fahrzeugen. Wie die Polizei mitteilt, kam es aus bisher unbekannten Gründen zu einer Frontalkollision zwischen zwei Autos. Ein nachfolgender dritter Wagen konnte nicht mehr rechtzeitig bremsen und prallte ebenfalls mit beiden anderen Unfallfahrzeugen zusammen.\nBei dem Unfall wurden zwei Personen verletzt, die Schwere der Verletzungen sind bislang nicht bekannt."
    results = search_in_text(query=query,text=title + exerpt)
    print("Matches:", results)
    results = search_in_text(query, text=title2 + expert2 + text2)
    print("Matches:", results)
    #test_data()
