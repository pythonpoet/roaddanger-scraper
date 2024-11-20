from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
#sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
import selenium
import logging
import time
import os
from pathlib import Path
from docx import Document


CURR_DIRECTORY = Path(__file__).parent

# Hanlding Logging CONFIGS
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)
# Set logging level for Selenium and other libraries to WARNING
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

def debugx(*args):
    logger.debug(" ".join(map(str,args)))

def infox(*args):
    logger.info(" ".join(map(str,args)))

class NexisWebScrapper:
    # Shoutout to: https://github.com/JayJhaveri1906/Nexis-Uni-Scraper/blob/main/NexisUniWebsiteScraper.py
    def __init__(self, link, valueToStart=1, N=0, BATCH_SIZE=250, query_word = "Hate Crime"):
        # maybe add btime, etime to dynamic the query

        # TODO: add beg time, end time, and also make link dynamic
        os.makedirs(f'{CURR_DIRECTORY}\\Downloads\\{query_word}_{valueToStart}', exist_ok=True)
        self.downloadLocation = f"{CURR_DIRECTORY}\\Downloads\\{query_word}_{valueToStart}"

        # Setting up chrome
        opts = ChromeOptions()
        #opts.add_argument("--window-size=1920,1080")    # window size
        
        prefs = {
            "download.default_directory": self.downloadLocation,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
        }
        opts.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=opts) # Initializing chrome selenium driver
        
        self.link = link  # Link with query
        
        self.N = N  # final number of articles
        self.valueToStart = valueToStart    # Starting point for range
        self.batchSize = BATCH_SIZE    # MAXIMUM Value = 500 (Due to lexis nexis restrictions)
                                # Minimum Value = 2, (Due to how i coded i lol)
                                # Recommended = 250, sometimes at 500, lexis uni decides to email you
                                # the results, but you are not even logged in, so that is just
                                # lost lmao.        
        infox("Initialized")


    def scraper(self, searchTerm: str, articleCount):
        self.search = self.driver.find_element(By.CSS_SELECTOR, "lng-expanding-textarea[placeholder='Geef termen, bronnen of bedrijven op']")
        self.search.click()
        self.search.send_keys(searchTerm + Keys.ENTER)
        for i in range(articleCount):
            time.sleep(5)
            selectall_button = self.driver.find_element(By.CSS_SELECTOR, "input[data-action='selectall']")
            selectall_button.click()
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            next_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-action='nextpage']")
            next_button.click()

        export = self.driver.find_element(By.CLASS_NAME, "icon la-Download")
        export.click()

    
    def login(self):
        # Make sure VPN is active
        # Just visiting the home page when UCSD VPN is active,
        # stores the session cookie in your browser which auto logs you in
        self.driver.get("http://www.nexisuni.com/")
        infox("Login Complete")

    def login2(self):
        # Has to be run in university network
        # Is re-routing to nexis uni and signs in by ip
        # use login
        self.driver.get("https://www.Nexis.com")
        time.sleep(5)
        access = self.driver.find_element(By.CLASS_NAME, "mipguest") # Only at Uni
        access.click()
        infox("Login Complete")


    # Makes sure the element is present before selecting the element
    def helper_find_element(self, xpath, time_limit=20) -> selenium.webdriver.remote.webelement.WebElement:
        return WebDriverWait(self.driver, time_limit).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def browse_(self, searchTerm: str, articleCount):
        self.search = self.driver.find_element(By.CSS_SELECTOR, "lng-expanding-textarea[placeholder='Geef termen, bronnen of bedrijven op']")
        self.search.click()
        self.search.send_keys(searchTerm + Keys.ENTER)
        for i in range(articleCount):
            time.sleep(5)
            selectall_button = self.driver.find_element(By.CSS_SELECTOR, "input[data-action='selectall']")
            selectall_button.click()
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            next_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-action='nextpage']")
            next_button.click()

        export = self.driver.find_element(By.CLASS_NAME, "icon la-Download")
        export.click()
    def changelangToEN(self): 
        # Actions button
        # Wait for the toggle button and click it to open the menu
        toggle_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='gnslanguagebutton']"))
        )
        toggle_button.click()

        # Wait for the dropdown menu to become visible
        menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//gnslanguagemenu"))
        )

        # Select the "EN - English (UK)" option
        english_uk_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//gnslanguagemenu//li/button[span[text()='EN - English (US)']]"))
        )
        english_uk_button.click()
        
        infox("Switched language to EN")
    
    def toggleHighSimilarity(self):
        # Actions button
        actionsButton = self.helper_find_element("//button[@id='resultlistactionmenubuttonhc-yk']")
        actionsButton.click()

        highSimiButton = self.helper_find_element("//ul[@class='nexisnewdedupe']//button[@data-action='changeduplicates' and @data-value='high']")

        # Off by default
        debugx("Similarity Level", self.helper_find_element("//button[contains(@class, 'la-Correct')]").get_attribute("data-value"))

        highSimiButton.click()  # causes a ajax request

        time.sleep(5)   # Even though I have used multiple layers of checking 
                        # if the element is present, it still errors 1 out of 10
                        # times... So to make sure we add this!
        
        
        ## WAITING FOR AJAX TO COMPLETE THE SOFT REFRESH BY MONITORING THE VALUE
        # turnedHigh = WebDriverWait(self.driver, 20).until(
        #     lambda driver: driver.find_element(By.XPATH, "//button[contains(@class, 'la-Correct')]")
        #                     .get_attribute("data-value") == "high"
        # )
        turnedHigh = WebDriverWait(self.driver, 20).until(
            lambda driver: self.helper_find_element("//button[contains(@class, 'la-Correct')]")
                            .get_attribute("data-value") == "high"
        )

        infox("Toggled to High Similarity!")
        # Changed to High from Off
        debugx("Similarity Level", self.helper_find_element("//button[contains(@class, 'la-Correct')]").get_attribute("data-value"))


        self.updateNumberOfArticles()   # Update the number of articles


    def updateNumberOfArticles(self):
        # wait for any ajax request to complete
        N_span = self.helper_find_element("//span[@data-actualresultscount]")
        self.N = int(N_span.get_attribute("data-actualresultscount"))
        infox("Updated Number of Articles to", self.N)

    
    def clickDownloadIcon(self):
        download_button = self.helper_find_element("//button[@data-qaid='toolbar_downloadopt']")
        download_button.click()
        infox("Clicked download button")


    def changeInputValue(self, valueToStart=1):
        inputText = self.helper_find_element("//input[@id='SelectedRange' and @placeholder]")
        inputText.clear()
        print(f"n: {self.N}, valueToStart: {valueToStart}, batchSize: {self.batchSize}")
        if (self.N - valueToStart + 1) < self.batchSize:    # if less than batch size
            range_text = str(valueToStart) + "-" + str(self.N)  # go till last element
        else:
            range_text = str(valueToStart) + "-" + str(valueToStart+1 + self.batchSize-1)  # go till batchSize

        inputText.send_keys(range_text)
        
        infox("Changed input value to", range_text)

    
    def selectWordFormat(self):
        wordInput = self.helper_find_element("//input[@type='radio' and @id='Docx']")
        wordInput.click()
        infox("Selected MS Word Format")


    def clickDownloadButton(self):
        downloadButton = self.helper_find_element("//button[@data-action='download']")
        downloadButton.click()
        infox("Clicked download button")


    def waitForSuccessfullProcessing(self):
        infox("Starting to Wait for Processing to be completed")
        while True:
            try:
                # Wait indefinitely until the "Download ready" element is found
                download_ready_element = self.helper_find_element("//span[contains(text(), 'Download ready')]", 60)
                infox("Processing is done!")
                break  # Exit the loop when the download is complete
            except TimeoutException:
                debugx("Still waiting for the processing to complete...")

        time.sleep(10)


    def waitForSuccessfullDownloading(self):
        infox("Starting to Wait for Download to be completed")
        dl_wait = True
        while dl_wait:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir(self.downloadLocation):
                if fname.endswith('.crdownload'):
                    dl_wait = True
        infox("Download Finished!, Closing")
        time.sleep(10)


    def runEntireSingleBatch(self, valueToStart = 1):
        self.login()
        self.driver.get(self.link)

        self.changelangToEN()
        time.sleep(1)

        #self.toggleHighSimilarity()
        time.sleep(1)

        self.clickDownloadIcon()
        time.sleep(1)

        # TODO Implement logic to partition self.N into batch sizes (use loop or multithreading?)
        # Problem: we need self.n after selecting high simi to know how to partition
        # It won't allow us to download repeatedly, we need new incognito session each time
        # So maybe need a parent script that finds self.n, then run child scripts to open
        # the new url directly and download in given batch range
        self.changeInputValue(valueToStart)
        time.sleep(1)
        
        self.selectWordFormat()
        time.sleep(1)

        self.clickDownloadButton()
        time.sleep(1)
        # Debug

        self.waitForSuccessfullProcessing()

        self.waitForSuccessfullDownloading()

        # input("waiting to close")
        self.driver.close()


    def getN(self):
        self.login()
        self.driver.get(self.link)
        self.changelangToEN()
        time.sleep(1)
        self.toggleHighSimilarity()

        self.driver.close()

        return self.N




if __name__ == "__main__":
    # Bias Incident
    link = "https://advance.lexis.com/search/?pdmfid=1519360&crid=6a96db27-ad51-49a8-9f5c-0ab19c3fb37b&pdsearchterms=(Unfall)+AND+(Verkehr)+AND+(Switzerland)&pdstartin=hlct%3A1%3A1&pdcaseshlctselectedbyuser=false&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdoriginatingpage=bisnexishome&pdqttype=and&pdquerytemplateid=&ecomp=hcdxk&prid=da498917-78b4-4a46-88cd-4b236f926eb7"
    query = "Verkehrs Unfall"

    # Bias Crime
    # link = "https://advance.lexis.com/search/?pdmfid=1519360&crid=a29c632f-84e1-45e7-8175-c3c6f03ae529&pdsearchterms=((Bias+W%2F2+Crime))+AND+((date+aft(06%2F01%2F2020))+AND+(DATE+BEF(12%2F31%2F2020)))+AND+new+york&pdstartin=hlct%3A1%3A1&pdcaseshlctselectedbyuser=false&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdoriginatingpage=search&pdqttype=and&pdquerytemplateid=&ecomp=hcdxk&prid=a907010f-8daf-4ab7-9725-f03cdd7d63ad"
    # query = "Bias Crime"
    
    # Hate Crime
    # link = "https://advance.lexis.com/search/?pdmfid=1519360&crid=a907010f-8daf-4ab7-9725-f03cdd7d63ad&pdsearchterms=((Hate+W%2F2+Crime))+AND+((date+aft(06%2F01%2F2020))+AND+(DATE+BEF(12%2F31%2F2020)))+AND+new+york&pdstartin=hlct%3A1%3A1&pdcaseshlctselectedbyuser=false&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdoriginatingpage=search&pdqttype=and&pdquerytemplateid=&ecomp=hcdxk&prid=ad6927ea-40c2-4c79-99ed-983e8f86fa13"
    # query = "Hate Crime"

    nexis_getN = NexisWebScrapper(link, query_word=query)
    
    infox("Running once to get Total number of articles")
    N = nexis_getN.getN()
    infox("Received N:", N)

    infox("Starting automated downloading Process")
    BATCH_SIZE = 250
    # TODO Look into Multi threading?
    for valueToStart in range(500, N+1, BATCH_SIZE): # move in increments of batch size
        infox("Running Batch", (valueToStart//BATCH_SIZE) + 1, "/", (N//BATCH_SIZE)+1)
        nexis = NexisWebScrapper(link, valueToStart, N, BATCH_SIZE, query)
        nexis.runEntireSingleBatch(valueToStart)
    
    infox("Finished Running!")