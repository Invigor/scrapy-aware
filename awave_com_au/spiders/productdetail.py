import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from awave_com_au.items import ProductDetailItem

class ProductDetail(CrawlSpider):
    name = 'productdetail'
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

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('/red-wine/', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow=('/page/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        productdetail = ProductDetailItem()
	productdetail['url'] = response.url
        productdetail['price'] = response.xpath('//*[@class="woocommerce-Price-amount amount"]/text()').extract_first()
        productdetail['name'] = response.xpath('//*[@class="woocommerce-loop-product__title"]/text()').extract_first()
        productdetail['description'] = response.xpath('//*[@class="woocommerce-Tabs-panel--description"]/text()').extract_first()
        productdetail['sku'] = response.xpath('//*[@class="sku"]/text()').extract_first()
        # product['rrp'] = response.xpath('//*[@class="woocommerce-loop-product__title"]/text()').extract_first()
        return productdetail
