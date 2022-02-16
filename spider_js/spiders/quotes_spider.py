import scrapy
from scrapy_selenium import SeleniumRequest


class QuotesSpider(scrapy.Spider):
	name = 'quotes'


	def start_requests(self):
		url = 'http://quotes.toscrape.com/js/'
		yield SeleniumRequest(url=url, callback=self.parse)


	def parse(self, response):

		for quote in response.css('div.quote'):
			yield {
				'quote': quote.css('span.text::text').get(),
				'author': quote.css('small.author::text').get(),
				'tags': quote.css('div.tags a.tag::text').getall(),
			}

		next_page = response.urljoin(response.css('li.next a::attr(href)').get())
		if next_page is not None:
			yield SeleniumRequest(url=next_page, callback=self.parse)

