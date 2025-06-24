# BookScraper: A Robust Scrapy Crawler with Proxies, User-Agent Rotation, and MySQL Integration

This is a web scraping project built using **Scrapy** that extracts book data from the site [books.toscrape.com](https://books.toscrape.com/).

---

## Features

| Feature | Description |
|--------|-------------|
|**User-Agent Rotation** | Custom middleware fetches 60 fake browser headers from [ScrapeOps API](https://scrapeops.io/), mimicking real users. |
|**Proxy Rotation** | Scrapy rotates through a list of public proxies to avoid getting blocked. |
|**Data Cleaning** | Cleans availability, rating, and numerical fields before saving. |
|**MySQL Integration** | Scraped items are inserted into a MySQL database using `mysql-connector-python`. |
|**Export Options** | Export data directly to `JSON`, `CSV`, or `XML` using `-O` flag. |

---

## Sample Data Fields Collected

- Title  
- Price  
- Availability  
- Category  
- Product Type  
- UPC  
- Tax  
- Reviews  
- Rating  
- Description  
- Product Page URL  

---

## Setup

```bash
# Clone the repo
git clone https://github.com/sushruta19/bookscraper.git
cd bookscraper

# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat   # On Windows(Command Prompt)
source venv/bin/activate    # On Linux(Bash)

# Install dependencies
pip install -r requirements.txt

# Run the helper script to generate your environment variables
python create_env.py
```

## Run
```bash
# Enter the main Scrapy project file
cd bookscraper

# Check available spiders
scrapy list

# Run the spider(Make sure your MYSQL DB is running!)
scrapy crawl bookspider

# To store the output in csv or json file
scrapy crawl bookspider -O output.json
scrapy crawl bookspider -O output.csv
```

This project is open-source and available under the [MIT License](LICENSE)
