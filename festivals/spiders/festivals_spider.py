from scrapy import Spider, Selector, Request
import re

from festivals.items import FestivalsItem


class FestivalsParser(Spider):
    name = 'festivals'
    allowed_domains = ['leguidedesfestivals.com']
    start_urls = ['http://www.leguidedesfestivals.com/index.php5?page=festivals-regions-grandes']
    url_prefix = 'http://www.leguidedesfestivals.com/'
    festival_link_xpath = '//a[contains(@class,"list-group-item") and .//img]/@href'
    festival_info_block_xpath = '//*[@id="fest"]/div[1]/div[2]'
    date_category_xpath = '//*[@id="fest"]/div[1]/div[2]/text()'
    date_xpath = '//*[@id="fest"]/div[1]/div[2]/h4/text()'
    category_xpath = '//*[@id="fest"]/div[1]/div[2]/text()'
    url_xpath =  '//*[@id="fest"]/div[1]/div[2]/strong[5]/a/@href'
    url_xpath2 = '//*[@id="fest"]/div[1]/div[2]/strong[4]/a/@href'
    facebook_xpath = '//*[@id="fest"]/div[1]/div[2]/a[1]/@href'
    twitter_xpath = '//*[@id="fest"]/div[1]/div[2]/a[2]/@href'
    address_info = '//*[@id="fest"]/div[2]/div[2]/text()'
    email_xpath = '//*[@id="fest"]/div[2]/div[3]/p/text()'
    address_xpath = '//*[@id="fest"]/div[2]/div[2]/font[1]/font/text()'
    zip_city_xpath = '//*[@id="fest"]/div[2]/div[2]/font[2]/font/text()'
    name_xpath = '//h3/text()'
    next_page_xpath = '//ul[@class="pagination"]/li/a/@href'
    region_links_xpath = '//div[@class="panel-body"]/div[@class="col-md-6"][2]/p/a/@href'

    def parse(self, response):
        xhs = Selector(response)
        region_links = xhs.xpath(self.region_links_xpath).extract()
        for region in region_links:
            yield Request(url=self.url_prefix + region + '&p=1', callback=self.parse_region, dont_filter=True)
        pass

    def parse_region(self, response):
        xhs = Selector(response)
        links = xhs.xpath(self.festival_link_xpath).extract()
        for link in links:
            yield Request(url=self.url_prefix + link, callback=self.parse_festival, dont_filter=True)
        if links:
            next_page = xhs.xpath(self.next_page_xpath).extract()[-1]
            if next_page not in response.url:
                yield Request(url=self.url_prefix + next_page, callback=self.parse, dont_filter=True)

    def parse_festival(self, response):
        xhs = Selector(response)
        info_block = xhs.xpath(self.festival_info_block_xpath)
        name = info_block.xpath(self.name_xpath).extract()[0]
        date = ''
        category = ''
        if len(xhs.xpath(self.date_xpath).extract()) == 0:
            decoded_str = info_block.extract()[0].split("br")[1]
            info = decoded_str.encode('utf-8')
            if info.startswith('>'):
                info = info[1:].strip(' \r\t\n')
            if info.endswith('<'):
                info = info[:-1]
            date = re.search(r'(\d+/\d+/\d+)', info).group(1)
            category = info.split(date)[1]
        else:
            date = xhs.xpath(self.date_xpath).extract()[0]
            category = self.compress_str(xhs.xpath(self.category_xpath).extract())
        if '\n' in category:
            category = ''
        url = ''
        url_check = xhs.xpath(self.url_xpath).extract()
        if url_check:
            url = url_check[0]
        else:
            url = xhs.xpath(self.url_xpath2).extract()[0]
        facebook_check = xhs.xpath(self.facebook_xpath).extract()
        facebook = ''
        if facebook_check:
            facebook = facebook_check[0]
            if facebook.startswith('https://https:'):
                facebook = facebook.replace('https://https://', 'https://')
        twitter_check = xhs.xpath(self.twitter_xpath).extract()
        twitter = ''
        if twitter_check:
            twitter = twitter_check[0]
        email = self.compress_str(xhs.xpath(self.email_xpath).extract(), True)

        info = xhs.xpath(self.address_info).extract()
        address = self.compress_str(info[0])
        city_zip = self.compress_str(info[1])
        if not re.findall(r"(\d{5})", city_zip):
            address = address + ' ' + city_zip
            city_zip = self.compress_str(info[2])
        zip = ''
        city = ''
        if city_zip == 'France':
            zip = address.split(' ')[0]
            city = address.split(zip)[1]
        else:
            zip = city_zip.split(' ')[0]
            city = self.compress_str(city_zip.split(zip)[1])
            if re.findall(r"(\d{5})", city):
                zip = self.compress_str(info[2]).split(' ')[0]
                city = self.compress_str(info[2]).split(' ')[1]
        is_region = 'nord-pas-de-calais' in response.request.headers.get('Referer', None)
        if len(twitter):
            facebook = facebook + ' ' + twitter
        festival = FestivalsItem()
        festival['FESTIVAL_NAME'] = name
        festival['EVENT_ON'] = date
        festival['CATEGORY'] = category
        festival['SOCIAL'] = facebook
        festival['EMAIL'] = email
        festival['ADDRESS'] = address
        festival['ZIP_CODE'] = zip
        festival['CITY'] = city
        festival['isRegion'] = is_region
        festival['page_url'] = response.url
        festival['URL'] = url
        return festival

    def compress_str(self, str, findEmail=False):
        if isinstance(str, list):
            for item in str:
                compressed = self.replace_chars(item)
                if len(compressed) > 0:
                    if findEmail:
                        if '@' in compressed:
                            return compressed
                        else:
                            continue
                    else:
                        return compressed
            return ''
        return self.replace_chars(str)

    def replace_chars(self, str):
        return str.strip(' \r\t\n').replace(u'\xa0', u' ')
