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
