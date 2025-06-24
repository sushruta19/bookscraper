# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        #strip whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        #switch to lowercase for category and product type
        field_names = ['category', 'product_type']
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.lower()
        
        #prices convert to float
        field_names = ['price_excl_tax', 'price_incl_tax', 'price', 'tax']
        for field_name in field_names:
            value = adapter.get(field_name)
            value = value.replace('£', '')
            adapter[field_name] = float(value)

        #availability => extract number of books if in stock
        value = adapter.get('availability')
        split_arr = value.split('(')
        if len(split_arr) < 2:
            adapter['availability'] = 0
        else:
            adapter['availability'] = int(split_arr[1].split()[0])
        
        #reviews convert str to int
        value = adapter.get('num_reviews')
        adapter['num_reviews'] = int(value)

        #ratings str to int
        value = adapter.get('rating')
        value = value.lower()
        if value == 'zero':
            adapter['rating'] = 0
        elif value == 'one':
            adapter['rating'] = 1
        if value == 'two':
            adapter['rating'] = 2
        if value == 'three':
            adapter['rating'] = 3
        if value == 'four':
            adapter['rating'] = 4
        if value == 'five':
            adapter['rating'] = 5
        
        return item
