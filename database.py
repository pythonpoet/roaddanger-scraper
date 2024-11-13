
import os
from supabase import create_client, Client
from keys import *
import re
import pycountry
from datetime import *
from postgrest.exceptions import APIError
import postgrest
from opencage.geocoder import OpenCageGeocode


geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    # Append the list if you use a new source here
dataOrigins = [
    "roaddanger",
    "lexisnexus",
    "newsapi"
]

def validate_country_name(country_name):
    # First, check if the input is an official country name
    country = pycountry.countries.get(name=country_name)
    if country:
        return country_name
    # If input is a country code, raise an error
    country_code = pycountry.countries.get(alpha_2=country_name.upper())
    if country_code:
        raise ValueError(f"'{country_name}' is a country code, not a full country name. Please use '{country_code.name}'.")
    # If input is neither, return not found
    raise ValueError(f"'{country_name}' is not recognized as a valid country name or code.")

def validate_date(date_str):
    """
    Validates if the given date_str matches the format 'YYYY-MM-DD' or optionally 'YYYY-MM-DD HH:MM:SS'.
    
    Args:
        date_str (str): The date string to validate.
    
    Raises:
        ValueError: If date_str does not match the expected format or if year, month, or day is missing.
        
    Returns:
        bool: True if date_str is valid.
    """
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


def validate_plain_text(text):
    """
    Validates that the input text does not contain HTML tags.
    
    Args:
        text (str): The text string to validate.
    
    Raises:
        ValueError: If the text contains HTML tags.
        
    Returns:
        bool: True if the text is plain and does not contain HTML tags.
    """
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

def validate_sitename(sitename):
    # Check if any of the parameters are None or empty
    if not sitename:
        raise ValueError("Parameter 'sitename' is required and cannot be empty.")
    return sitename
def validate_url( url):
    # Check if any of the parameters are None or empty

    if not url:
        raise ValueError("Parameter 'url' is required and cannot be empty.")
    
    return url

def validate_dataOrigin(dataOrigin):

    if not dataOrigin in dataOrigins:
        raise Exception(f'dataOrigin: {dataOrigin} is not in {dataOrigins} append new dataOrigin in List')
    
    return dataOrigin




def get_country(latitude, longitude):
    """ Function returns country name provided lat and long
    """
    try:

        results = geocoder.reverse_geocode(latitude, longitude, language='en',)
        return results[0]['components']['country']
    
    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred for coordinates ({latitude}, {longitude}): {str(e)}")

def logError(log_entry, logfile_path="logfile.txt"):
    with open(logfile_path, "a") as logfile:
        logfile.write(log_entry + "\n")






class ImagineAllTheData():
    # Init class & suprabase database
    def __init__(self):

        # Always keep credentials in keys.py
        url: str = SUPABASE_URL
        key: str = SUPABASE_KEY
        self.supabase: Client = create_client(url, key)


    # push news-article under /country/publisher/articleName to avoid name collition
    def pushArticle(self, headline: str, alltext:str, sitename: str, url:str, country:str, dateTime:str, dataOrigin: str, articleID:str = None):


        article =  {
        "id": articleID,
        "headline": validate_plain_text(headline),
        "dateTime": validate_date(dateTime),
        "alltext": validate_plain_text(alltext),
        "sitename": validate_sitename(sitename),
        "url": validate_url(url),
        "country": validate_country_name(country),
        "dataOrigin" : validate_dataOrigin(dataOrigin),
        # Specify format version. If changes are made incriment version tag
        "version": 1
        }
        try:
            response = self.supabase.table("article_prototype").insert([article]).execute()
        except postgrest.exceptions.APIError as e:
            print("API Error:", e)
            print("Response content:", e.response.content if hasattr(e, 'response') else "No response content")

    def get_article_by_country(country: str):
        return self.supabase.table("article_prototype").select("*").eq("country", country).execute()
    # pull news-article under /country/publisher/articleName
    def pullArticle(self, country: str, publisher: str, articleName: str):
        pass

    # Check first if document exist; create document first before doing the compute to avoid double compute of an article
    def checkIfComputeExists(self, country: str, publisher: str, articleName: str):
        pass
    # push compute
    def pushCompute(self, country: str, publisher: str, articleName: str):
        if self.checkIfComputeExists(country, publisher, articleName):
            # TODO
            raise Exception("Not implemented")

        pass
    
    def pullCompute(self, country: str, publisher: str, articleName: str):
        pass

    

if __name__ == "__main__":
    db = ImagineAllTheData()

    # Testing Coutry name
    try:
        validate_country_name("NL")  # Should raise an error
    except ValueError as e:
        print(e)

    try:
        validate_country_name("Netherlands")  # Should print that it's valid
    except ValueError as e:
        print(e)

    # Testing Date
    try:
        validate_date("2023-11-12 15:45:00")  # Should return True
        print("Valid datetime.")
    except ValueError as e:
        print(e)

    try:
        validate_date("2023-11")  # Should return True
        print("Valid datetime.")
    except ValueError as e:
        print(e)

    try:
        validate_date("2023/11/12 15:45:00")  # Should raise ValueError
    except ValueError as e:
        print(e)

    # Testing plain text
    try:
        validate_plain_text("This is plain text.")  # Should return True
        print("Valid plain text.")
    except ValueError as e:
        print(e)

    try:
        validate_plain_text("This text contains <b>HTML</b> tags.")  # Should raise ValueError
    except ValueError as e:
        print(e)
   
