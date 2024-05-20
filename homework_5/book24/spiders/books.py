import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["book24.ru"]
    start_urls = ["https://book24.ru/catalog/samoobrazovanie-i-razvitie-4560/"]

    custom_settings={ 'FEED_URI': "aliexpress_%(time)s.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        
        books = response.xpath('//article')
        for book in books:
            name = book.xpath('.//text()').get()
            autor = book.xpath('.//div[2]/div/a/text()').get()
            yield{
                'name' : name,
                'autor' : autor,
            }

            