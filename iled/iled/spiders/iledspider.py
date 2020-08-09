import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from iled.items import IledItem


class IledSpider(scrapy.spiders.CrawlSpider):
    """Паук"""

    name = 'iled'
    allowed_domains = ['iledebeaute.ru']
    start_urls = ['https://iledebeaute.ru/shop/brands/']
    # со стратовой страницы собрали все ссылки и побежали по ним parse_item
    rules = [
        Rule(LinkExtractor(allow='/shop/brands/\w+/'), callback='parse_item'),
    ]

    def parse_item(self, response):
        div = response.xpath('//div[@class="_js-mobile-showcase-container b-mobile-showcase cf"]')
        items = div.xpath('div')
        for item in items:
            product = IledItem()
            product['brand'] = item.xpath('p[@class="b-showcase__item__brand"]/text()').get().strip()
            product['title'] = item.xpath('p[@class="b-showcase__item__link"]/a/text()').get().strip()
            product['price'] = item.xpath('p[@class="b-showcase__item__price"]/span/text()').get().strip()
            product['url'] = item.xpath('a/@href').get().strip()
            yield product

        # после того как собрали с 1 страници бренда собираем все ссылки и идем по ним
        try:
            nav = response.xpath('//nav[@class="b-pagination"]')[0]
        except IndexError:
            nav = response.xpath('//nav[@class="b-pagination"]')

        pages = nav.xpath('.//a/@href').getall()
        abs_p = get_iter_abs_pages(pages)
        for p in abs_p:
            if p == response.url:
                try:
                    yield scrapy.Request(next(abs_p), callback=self.parse_item)
                except StopIteration:
                    continue


def get_iter_abs_pages(pages):
    for p in pages:
        yield 'https://iledebeaute.ru' + p
