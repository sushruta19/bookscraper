# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

# do this if you dont wanna use pipelines
# def serialize_price(value):
#     return f'£ {str(value)}'

class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    category=scrapy.Field()
    price=scrapy.Field()
    tax=scrapy.Field()
    price_excl_tax = scrapy.Field() #serializer= serialize_price
    price_incl_tax =scrapy.Field()
    availability=scrapy.Field()
    num_reviews=scrapy.Field()
    rating=scrapy.Field()
    description=scrapy.Field()
    