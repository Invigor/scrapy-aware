import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from awave_com_au.items import ProductListItem

class ProductList(CrawlSpider):
    name = 'productlist'
    allowed_domains = ['awave.com.au']
    start_urls = [
      	'https://www.awave.com.au/product-category/outboard/',
	'https://www.awave.com.au/product-category/',
        'https://www.awave.com.au/product-category/monitoring/',
	'https://www.awave.com.au/product-category/consoles/',
	'https://www.awave.com.au/product-category/instruments/',
	'https://www.awave.com.au/product-category/computer-music/',
	'https://www.awave.com.au/product-category/accessories/'
	]

#    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('/red-wine/', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
#        Rule(LinkExtractor(allow=('/page/', )), callback='parse_item'),
#    )

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        product = ProductListItem()

        # product['url'] = response.url
	# prices = response.xpath('//*[@class="woocommerce-Price-currencySymbol"]/following-sibling::text()').extract()
	# names = response.xpath('//*[@class="woocommerce-loop-product__title"]/text()').extract()
	producturls = response.css('.woocommerce-LoopProduct-link::attr(href)').extract() 

	# print(prices)
	# print(names)
	# print(producturls)

	# print('Products on this page: %s',len(names))

	for i in xrange(0,len(producturls)):
	   # if len(prices) > i:
           #    product['price'] = prices[i]
	   # else:
	   #     product['price'] = '0.00'
           # product['name'] = names[i]
           # if len(prices) > i:
           product['producturl'] = producturls[i]
	   #else:
	   #    product['producturl'] = ''
	   # self.logger.info('Processing:! %s', names[i])
           yield product

	next_page = response.css('.next::attr(href)').extract_first()
        if next_page is not None:
           next_page = response.urljoin(next_page)
           yield scrapy.Request(next_page, callback=self.parse)
