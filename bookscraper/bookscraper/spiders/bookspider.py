import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            yield {
                'name':book.css('a::text').get(),
                'price':book.css('p.price_color::text').get(),
                'availability':' '.join(book.css('p.instock::text').getall()).strip(),
                'rating': book.css('p.star-rating::attr(class)').get().split()[-1],
                'url': "https://books.toscrape.com/"+book.css('h3 a::attr(href)').get()
            }
