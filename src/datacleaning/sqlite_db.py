import sqlite3
from datetime import datetime
import re
import random

# Append dataOrigin here
dataOrigins = [
    "roaddanger",
    "lexisnexus",
    "newsapi"
]
def pushArticle(connection, headline, alltext, sitename, url, country, dateTime, dataOrigin, articleID=None):
    """
    Push an article to the SQLite database and validate inputs
    """
    create_article_table(connection=connection)
    # Validation functions
    def validate_plain_text(text):
            # Regular expression to detect HTML tags
        html_pattern = re.compile(r'<.*?>')

        # Check if any HTML tags are found
        if html_pattern.search(text):
            raise ValueError(f"Only text allowed, you entered: {text}")

        if text is None:
            raise ValueError("The text provides is of NoneType")
        if text == "":
            raise ValueError("Empty string provided")
        return text
    def validate_date(date_str:str):
    # List of acceptable formats: date only or date with optional time
        formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]  
        for fmt in formats:
            try:
                # Try to parse the date_str with each format
                datetime.strptime(date_str, fmt)
                return date_str
            except ValueError:
                # Continue to the next format if there's a ValueError
                continue
        # If no formats matched, raise an error
        raise ValueError(f"'{date_str}' is not in a valid format. Expected 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.") 

    def validate_sitename(value):
        return value.strip()

    def validate_url(value):
        if value.startswith("http://") or value.startswith("https://"):
            return value
        raise ValueError(f"Invalid URL: {value}")

    def validate_country_name(value):
        return value.strip()

    def validate_dataOrigin(dataOrigin):
        if not dataOrigin in dataOrigins:
            raise Exception(f'dataOrigin: {dataOrigin} is not in {dataOrigins} append new dataOrigin in List')
        return dataOrigin

    # Create a unique ID if none is provided
    article_id = articleID or f"{country}/{sitename}/{headline.replace(' ', '_')}"

    # Prepare the article data
    article = {
        "id": article_id,
        "headline": validate_plain_text(headline),
        "dateTime": validate_date(dateTime),
        "alltext": validate_plain_text(alltext),
        "sitename": validate_sitename(sitename),
        "url": validate_url(url),
        "countryid": validate_country_name(country),
        "dataOrigin": validate_dataOrigin(dataOrigin),
        "version": 1
    }

    # Insert the article into the database
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO articles (id, headline, dateTime, alltext, sitename, url, countryid, dataOrigin, version)
        VALUES (:id, :headline, :dateTime, :alltext, :sitename, :url, :countryid, :dataOrigin, :version)
        """

        cursor.execute(insert_query, article)
        connection.commit()
        
    except sqlite3.IntegrityError:
        print(f"Article with ID '{article_id}' already exists.")
    except sqlite3.Error as e:
        print(f"Error inserting article: {e}")

def get_table(connection, table:str,countryid:str=None, random_sample_size: int=None):
    """
    Retrieve table, filter by coutryid and limit article output with random_sample_size
    
    
    Parameters:
        connection (sqlite3.Connection): SQLite database connection object.
        countryid (str): The country ID to filter crashes.
        random_sample_size (int): The number of random rows to retrieve.
        
    Returns:
        list[dict]: A list of dictionaries representing the random sample of table entries.
    """
    cursor = connection.cursor()

    if countryid == None and random_sample_size == None:
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Fetch column names for creating dictionary output
        column_names = [description[0] for description in cursor.description]

        # Convert rows to list of dictionaries
        results = [dict(zip(column_names, row)) for row in rows]
        return results
    elif random_sample_size == None:
        query = f"SELECT * FROM {table} WHERE countryid = ?"
        cursor.execute(query, (countryid,))
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]
        return results
    elif countryid == None and random_sample_size != None:
        raise Exception("Error: countryid NoneType and ramdom_sample_size non NoneType doesn't make any sense :(")

    
    # Query to retrieve all rows matching the country ID
    query = f"SELECT * FROM {table} WHERE countryid = ?"
    cursor.execute(query, (countryid,))
    rows = cursor.fetchall()
    
    # Fetch column names for creating dictionary output
    column_names = [description[0] for description in cursor.description]
    
    # Shuffle rows and get a random sample of specified size
    random_sample = random.sample(rows, min(random_sample_size, len(rows)))
    
    # Convert rows to list of dictionaries
    results = [dict(zip(column_names, row)) for row in random_sample]
    return results


def create_article_table(connection):
    """
    Create the SQLite table to store article data if it does not exist.
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            headline TEXT NOT NULL,
            dateTime TEXT NOT NULL,
            alltext TEXT NOT NULL,
            sitename TEXT NOT NULL,
            url TEXT NOT NULL,
            countryid TEXT NOT NULL,
            dataOrigin TEXT NOT NULL,
            version INTEGER NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")



def create_crash_table(connection, crash_data):
    """
    Create tables and insert data based on the specified schema.
    """
    cursor = connection.cursor()

    # Create the `crashes` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crashes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            text TEXT,
            date TEXT NOT NULL,
            latitude ,
            longitude ,
            unilateral ,
            pet INTEGER ,
            trafficjam INTEGER ,
            publishedtime TEXT NOT NULL,
            countryid TEXT NOT NULL
        );
    """)
    # Insert data into the `crashes` table
    article_query = """
        INSERT INTO crashes (id, title, text, date, latitude, longitude, unilateral, pet, trafficjam, publishedtime, countryid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(article_query, (
        crash_data["id"],
        crash_data["title"],
        crash_data["text"],
        crash_data["date"],
        crash_data["latitude"],
        crash_data["longitude"],
        crash_data["unilateral"],
        crash_data["pet"],
        crash_data["trafficjam"],
        crash_data["publishedtime"],
        crash_data["countryid"]
    ))
    # Commit the transaction
    connection.commit()
    

def create_person_table(connection, person, crash_id):
    """
    Create and insert person table

    """
    cursor = connection.cursor()

    # Create the `persons` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            groupid INTEGER,
            transportationmode INTEGER NOT NULL,
            health INTEGER NOT NULL,
            child INTEGER NOT NULL,
            underinfluence INTEGER NOT NULL,
            hitrun INTEGER NOT NULL,
            crash_id INTEGER NOT NULL,
            FOREIGN KEY (crash_id) REFERENCES crash (id) ON DELETE CASCADE
        );
    """)

    
    # Insert data into the `persons` table
    person_query = """
        INSERT INTO persons (id, groupid, transportationmode, health, child, underinfluence, hitrun, crash_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(person_query, (
        person["id"],
        person["groupid"],
        person["transportationmode"],
        person["health"],
        person["child"],
        person["underinfluence"],
        person["hitrun"],
        crash_id
    ))

    # Commit the transaction
    connection.commit()

def roaddanger_clean_url(url:str ):
    # Replace escaped \/ with /
    return re.sub(r"\\/", "/", url)

# Example usage
if __name__ == "__main__":
    # Sample data
    crash_data = {
        "id": 16787,
        "title": "Automobilist ramt boom langs Kanaal A in Emmer-Compascuum",
        "text": "",
        "date": "2024-11-05T00:00:00+01:00",
        "latitude": 52.804979,
        "longitude": 6.9878,
        "unilateral": 1,
        "pet": 0,
        "trafficjam": 0,
        "persons": [
            {
                "id": 42278,
                "groupid": None,
                "transportationmode": 5,
                "health": 2,
                "child": 0,
                "underinfluence": 0,
                "hitrun": 0
            }
        ],
        "articles": [
            {
                "id": 19279,
                "sitename": "www.ad.nl",
                "publishedtime": "2024-11-05 00:00:00",
                "url": "https:\/\/www.ad.nl\/112-nieuws-emmen\/automobilist-ramt-boom-langs-kanaal-a-in-emmer-compascuum~a7c0f34d\/",
                "urlimage": "https:\/\/images0.persgroep.net\/rcs\/Ap0f0yjiOr48TJN5RQV598wgK6I\/diocontent\/250305242\/_fill\/1200\/630\/?appId=21791a8992982cd8da851550a453bd7f&quality=0.7",
                "title": "Automobilist ramt boom langs Kanaal A in Emmer-Compascuum",
                "alltext": "Op de Kanaal A NZ in Emmer-Compascuum is een automobilist dinsdagochtend tegen een boom aan gereden. De bestuurder is behandeld door ambulancepersoneel.\n\n112Redactie 05-11-24, 06:35 Laatste update: 07:14\nHet ongeval gebeurde rond half zeven in de ochtend. Er waren geen andere weggebruikers bij het ongeval betrokken. Hoe het komt dat de auto van de weg raakte, is niet bekend.",
                "summary": "Op de Kanaal A NZ in Emmer-Compascuum is een automobilist dinsdagochtend tegen een boom aan gereden. De bestuurder is behandeld door ambulancepersoneel."
            }
        ],
        "publishedtime": "2024-11-05T14:10:01+01:00",
        "countryid": "NL"
    }

    # Connect to SQLite database
    connection = sqlite3.connect("david_data.db")

    try:
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

        print(get_table(connection, "articles"))

    finally:
        connection.close()

