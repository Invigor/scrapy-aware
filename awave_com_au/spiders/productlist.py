import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from awave_com_au.items import ProductListItem

class ProductList(CrawlSpider):
    name = 'productlist'
    allowed_domains = ['awave.com.au']
    start_urls = ['https://www.awave.com.au/product-category/microphones/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('/red-wine/', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/page/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        product = ProductListItem()
	product['url'] = response.url
        product['price'] = response.xpath('//*[@class="woocommerce-Price-amount amount"]/text()').extract()
        product['name'] = response.xpath('//*[@class="woocommerce-loop-product__title"]/text()').extract()
        product['producturl'] = response.css('.woocommerce-LoopProduct-link::attr(href)').extract()
        return product
