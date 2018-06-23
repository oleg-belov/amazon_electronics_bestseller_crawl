import scrapy


class ElektronikBestellersSpider(scrapy.Spider):
    name = "elektronik_bestellers"
    start_url = 'https://www.amazon.de/gp/bestsellers/ce-de/ref=zg_bs_nav_0/261-1162755-1928137#1'
    count = 1

    def start_requests(self):
        act = getattr(self, 'act', None)

        if not act is None and act == 'dowland':
            yield scrapy.Request(url=self.start_url, callback=self.dowland_and_save_page, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 2}
                }
            })
        else:
            yield scrapy.Request(url=self.start_url, callback=self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 2}
                }
            })

    def parse(self, response):
        for item in self.get_items(response):
            yield {
                'asin': self.extract_asin(item),
                'prodName': self.extract_prod_name(item),
                'price': self.extract_price(item),
                'numView': self.extract_num_view(item),
                'numStars': self.extract_num_stars(item)
            }

        next_page = self.get_next_page(response)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def get_items(self, response):
        return response.css('#zg-ordered-list > li')

    def extract_asin(self, item):
        return item.css('span > div > span > a::attr(href)').extract_first().split('/dp/')[1].split('?')[0]

    def extract_prod_name(self, item):
        result = item.css(
            'span > div > span > a > div::attr(title)').extract_first()

        if not result:
            result = item.css(
                'span > div > span > a > div::text').extract_first()
        if not result is None:
            result = result.strip()

        return result

    def extract_price(self, item):
        return item.css('span > div > span > div.a-row > a > span > span::text').extract_first()

    def extract_num_view(self, item):
        result = item.css(
            'span > div > span > div.a-icon-row.a-spacing-none > a.a-size-small.a-link-normal::text').extract_first()

        try:
            if not result is None:
                return int(result)
            return result
        except ValueError:
            return result

    def extract_num_stars(self, item):
        result = item.css(
            'span > div > span > div.a-icon-row.a-spacing-none > a:nth-child(1) > i > span::text').extract_first()

        try:
            if not result is None:
                result = result[0:3]

                return float(result)
            return result
        except ValueError:
            return result

    def dowland_and_save_page(self, response):
        filename = 'page-%s.html' % self.count
        self.count = self.count + 1

        with open(filename, 'wb') as f:
            f.write(response.body)

        next_page = self.get_next_page(response)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.dowland_and_save_page)

    def get_next_page(self, response):
        return response.css(
            '#zg-center-div > div.a-row.a-spacing-top-mini > div > ul > li:last-child > a::attr(href)').extract_first()
