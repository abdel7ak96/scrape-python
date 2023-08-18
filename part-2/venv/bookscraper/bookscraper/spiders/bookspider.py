import scrapy


class BookspiderSpider(scrapy.Spider):
	name = "bookspider"
	allowed_domains = ["books.toscrape.com"]
	start_urls = ["https://books.toscrape.com/"]

	def parse(self, response):
		books = response.css('article.product_pod')
		for book in books:
			relative_url = book.css('h3 a').attrib['href']
			if 'catalogue/' in relative_url:
				book_url = 'https://books.toscrape.com/' + relative_url
			else:
				book_url = 'https://books.toscrape.com/catalogue/' + relative_url
			yield response.follow(book_url, callback = self.parse_book_page)
		
		next_page = response.css('li.next a').attrib['href']
		if next_page is not None:
			if 'catalogue/' in next_page:
				next_page_url = 'https://books.toscrape.com/' + next_page
			else:
				next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
			yield response.follow(next_page_url, callback = self.parse)
		
	def parse_book_page(self, response):
		table_rows = response.css('table tr')
		yield {
			'title': response.css('.col-sm-6.product_main h1::text').get(),
			'category': response.css('ul.breadcrumb :nth-child(3) a ::text').get(),
			'description': response.css('#product_description + p::text').get(),
			'price': response.css('p.price_color::text').get(),
			'product_type': table_rows[1].css('td ::text').get(),
			'price_excl_tax': table_rows[2].css('td ::text').get(),
			'price_incl_tax': table_rows[3].css('td ::text').get(),
			'tax': table_rows[4].css('td ::text').get(),
			'availability': table_rows[5].css('td ::text').get(),
			'rating': response.css('p.star-rating').attrib['class'].split(' ')[1],
			'url': response.url
		}

	

	