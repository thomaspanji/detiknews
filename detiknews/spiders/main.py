from email.policy import default
import imp
import scrapy
from scrapy.exceptions import CloseSpider

class DetikSpider(scrapy.Spider):
    name = 'detiknews'
   
    start_urls = [
        "https://www.detik.com/search/searchall?query=kementerian+pupr",
        'https://www.detik.com/search/searchall?query=kementerian+kelautan',
        "https://www.detik.com/search/searchall?query=kementerian+agama",
        "https://www.detik.com/search/searchall?query=kementerian+ham",
        'https://www.detik.com/search/searchall?query=kementerian+kesehatan',
        "https://www.detik.com/search/searchall?query=kementerian+keuangan",
        "https://www.detik.com/search/searchall?query=kementerian+kominfo",
        'https://www.detik.com/search/searchall?query=kementerian+sosial'
    ]

    def parse(self, response):
        news_links = response.css('article a')
        yield from response.follow_all(news_links, self.parse_news)

        pagination_links = response.css('div.paging a.last')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_news(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_with_css_tag(query):
            return response.css(query).getall()

        def extract_author(query):
            return response.css(query).re(r'(\w*\s?\w*\S?\w*) - (\w*)')[0]
            
        yield {
            'title': extract_with_css('h1.detail__title::text'),
            'category': extract_with_css('div.page__breadcrumb a::text'),
            'author': extract_author('div.detail__author::text'),
            'posted': extract_with_css('div.detail__date::text'),
            'tags': extract_with_css_tag('div.nav a.nav__item::text'),
        }

