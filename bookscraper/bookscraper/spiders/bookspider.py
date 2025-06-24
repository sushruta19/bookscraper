import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    
    # custom_settings = {
    #     'FEEDS' : {
    #         'booksCleanData.json' : {'format': 'json', 'overwrite': True} 
    #     }
    # }

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            # book_url = "https://books.toscrape.com/" + relative_url
            book_url = response.urljoin(relative_url)
            yield response.follow(
                book_url, 
                callback=self.parse_book_page
            )
            
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(
                next_page_url, 
                callback=self.parse  
            )

    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        book_item = BookItem()
        # this not only extracts the data
        # it also decides the order of fields in json or csv file
        book_item['url']= response.url
        book_item['title']= response.css('.product_page h1::text').get()
        book_item['upc'] = table_rows[0].css('td::text').get()
        book_item['product_type']= table_rows[1].css('td::text').get()
        book_item['category']= response.css('ul.breadcrumb li:nth-child(3) a::text').get()
        book_item['price']= response.css('p.price_color ::text').get()
        book_item['tax'] = table_rows[4].css('td::text').get()
        book_item['price_excl_tax']= table_rows[2].css('td::text').get()
        book_item['price_incl_tax']= table_rows[3].css('td::text').get()        
        book_item['availability']= table_rows[5].css('td::text').get()
        book_item['num_reviews']= table_rows[6].css('td::text').get()
        book_item['rating']= response.css('p.star-rating::attr(class)').get().split()[-1]
        book_item['description']= response.css('div#product_description + p::text').get()
        
        yield book_item