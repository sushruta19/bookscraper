# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class CleanDataPipeline:
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

# putting data in mysql db server
import mysql.connector
import os
from dotenv import load_dotenv

class SaveToMySQLPipeline:
    def __init__(self):
        load_dotenv()
        try:
            print("Connecting with SQL...")
            self.conn = mysql.connector.connect(
                host = os.getenv('MYSQL_HOST'),
                user = os.getenv('MYSQL_USER'),
                password = os.getenv('MYSQL_PASSWORD'),
                database = os.getenv('MYSQL_DATABASE'),
                use_pure = True
            )
        except Exception as e:
            print("MySQL connection error:", repr(e))
            raise SystemExit
        print("SQL Connection Successful!")
        self.cur = self.conn.cursor()

        self.cur.execute(
        """CREATE TABLE IF NOT EXISTS books(
            id INT NOT NULL auto_increment,
            url VARCHAR(255),
            title TINYTEXT,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL,
            tax DECIMAL,
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            availability INT,
            num_reviews INT,
            rating INT,
            description TEXT,
            PRIMARY KEY(id)
            )""")
    
    def process_item(self, item, spider):
        #insert sql commands
        self.cur.execute("""
            INSERT INTO books (
            url,
            title,
            upc,
            product_type,
            category,
            price,
            tax,
            price_excl_tax,
            price_incl_tax,
            availability,
            num_reviews,
            rating,
            description
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s)""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["category"],
            item["price"],
            item["tax"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["availability"],
            item["num_reviews"],
            item["rating"],
            str(item["description"] or "No Description")  
        ))

        self.conn.commit()
        return item #returning item since it can be used by other pipeline
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
