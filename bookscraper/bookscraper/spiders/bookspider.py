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
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)
