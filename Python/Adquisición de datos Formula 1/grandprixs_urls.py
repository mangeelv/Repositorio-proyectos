import re
import scrapy
import json
import os
from scrapy.crawler import CrawlerProcess




def obtain_urls():
    """Ejecuta el spider para obtener las urls de los report de cada carrera de un año y 
las guarda en un json por año."""

    process = CrawlerProcess()
    process.crawl(PrixSpider)
    process.start(stop_after_crawl=False)
    


    
class PrixSpider(scrapy.Spider):
    
    name = "GrandPrixs"
    start_urls = ["https://en.wikipedia.org/wiki/2012_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2013_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2014_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2015_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2016_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2017_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2018_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2019_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2020_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2021_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2022_Formula_One_World_Championship",
                  "https://en.wikipedia.org/wiki/2023_Formula_One_World_Championship",
    ]


    def parse(self, response):
        
        expected_name = "List of Formula One Grands Prix" 
        
        try:
            
            repetition = 0
            table_number = 0
        
            while expected_name != response.css("table")[table_number].css("tr")[0].css("a::attr(title)").get() or repetition != 2: # In case there are two tables with the same name
                table_number += 1
                
                if expected_name == response.css("table")[table_number].css("tr")[0].css("a::attr(title)").get() and len(response.css("table")[table_number].css("tr").getall()) > 15: # verify the length of the table to avoid the table with the same name but with no information
                    repetition += 1
                    
        except IndexError: # In case there is only one table with the expected name
            
            table_number = 0
            
            while expected_name != response.css("table")[table_number].css("tr")[0].css("a::attr(title)").get():
                table_number += 1
                
        table = response.css("table")[table_number]

        races = []
        
        for i in range(1,len(table.css("tr"))-1): 
            report_title = table.css("tr")[i].css("a::attr(title)")[-1].get() # Grand Prix
            report_page = table.css("tr")[i].css("a::attr(href)")[-1].get() # URL
            report_url = response.urljoin(report_page)

            races.append({"Grand Prix": report_title, "URL": report_url})
        
        year_pattern = re.compile(r"/(\d{4})_Formula_One_World_Championship") # Extract the year from the url
        match = year_pattern.search(response.url)
        year = match.group(1)

        os.makedirs("Yearly grandprixs reports",exist_ok=True) # Create a folder to save the info
        os.makedirs(f"Yearly grandprixs reports/{year}",exist_ok=True) # Create a folder per year

        with open(f"Yearly grandprixs reports/{year}/Grandprix_urls_{year}.json", "w", encoding = "utf-8") as file: # Save the json file
            json.dump(races,file,ensure_ascii = False, indent = 2)
            
if __name__ == "__main__":
    obtain_urls()