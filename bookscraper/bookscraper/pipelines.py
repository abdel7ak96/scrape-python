# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
	def process_item(self, item, spider):
		adapter = ItemAdapter(item)

		# Strip all whitespaces from description
		value = adapter.get('description')
		adapter['description'] = value.strip()

		# Category and product types transform to lowercase
		lowercase_keys = ['category', 'product_type']
		for lowercase_key in lowercase_keys:
			value = adapter.get(lowercase_key)
			adapter[lowercase_key] = value.lower()

		# Convert price to float
		price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
		for price_key in price_keys:
			value = adapter.get(price_key)
			value = value.replace('£', '')
			adapter[price_key] = float(value)

		# Extract number of available books
		availability_string = adapter.get('availability')
		split_string_array = availability_string.split('(')
		if len(split_string_array) < 2:
			adapter['availability'] = 0
		else:
			availability_array = split_string_array[1].split(' ')
			adapter['availability'] = int(availability_array[0])

		# TODO: Add 'num_reviews' field to my item
		# Convert number of reviews from string to int
		# num_reviews_string = adapter.get('num_reviews')
		# adapter['num_reviews'] = int(num_reviews_string)
		
		# Convert stars rating into an integer
		stars_rating = adapter.get('rating')
		stars_text_value = stars_rating.lower()
		if stars_text_value == 'zero':
			adapter['rating'] = 0
		elif stars_text_value == 'one':
			adapter['rating'] = 1
		elif stars_text_value == 'two':
			adapter['rating'] = 2
		elif stars_text_value == 'three':
			adapter['rating'] = 3
		elif stars_text_value == 'four':
			adapter['rating'] = 4
		elif stars_text_value == 'five':
			adapter['rating'] = 5

		return item

import mysql.connector

class SaveToMySQLPipeline:
	def __init__(self):
		self.conn = mysql.connector.connect(
			host = 'localhost',
			user = 'root',
			password = '',
			database = 'books'
		)

		## Create a cursor that used to execute commands
		self.cur = self.conn.cursor()

		## Create books table if not exists
		self.cur.execute("""
		CREATE TABLE IF NOT EXISTS books(
			id INT NOT NULL AUTO_INCREMENT,
			title TEXT,
			category VARCHAR(255),
			description TEXT,
			price DECIMAL,
			product_type VARCHAR(255),
			price_excl_tax DECIMAL,
			price_incl_tax DECIMAL,
			tax DECIMAL,
			availability DECIMAL,
			rating INTEGER,
			url VARCHAR(255),
			PRIMARY KEY (id)
		)
		""")

	def process_item(self, item, spider):
		## Define insert statement
		self.cur.execute("""INSERT INTO BOOKS (
				title,
				category,
				description,
				price,
				product_type,
				price_excl_tax,
				price_incl_tax,
				tax,
				availability,
				rating,
				url
			) values (
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
				%s
			)""",
				(
					item["title"],
					item["category"],
					str(item["description"][0]),
					item["price"],
					item["product_type"],
					item["price_excl_tax"],
					item["price_incl_tax"],
					item["tax"],
					item["availability"],
					item["rating"],
					item["url"],
				)
			)

		self.conn.commit()
		return item


		def close_spider(self, spider):
			## Close cursor & connection to database
			self.cur.close()
			self.conn.close()