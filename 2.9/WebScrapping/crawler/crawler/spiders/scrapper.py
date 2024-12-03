# search by CSS
# import scrapy
# import json
#
#
# class ScrapperSpider(scrapy.Spider):
#     name = "scrapper"
#     allowed_domains = ["quotes.toscrape.com"]
#     start_urls = ["http://quotes.toscrape.com"]
#
#     def __init__(self, *args, **kwargs):
#         super(ScrapperSpider, self).__init__(*args, **kwargs)
#         self.authors = []
#         self.quotes = []
#
#     def parse(self, response):
#         for author_link in response.css('small.author + a::attr(href)').extract():
#             yield scrapy.Request(response.urljoin(author_link), callback=self.parse_author)
#
#         for quote in response.css('div.quote'):
#             quote_text = quote.css('span.text::text').get()
#             quote_author = quote.css('small.author::text').get()
#
#             quote_data = {
#                 'text': quote_text,
#                 'author': quote_author,
#             }
#
#             self.quotes.append(quote_data)
#             yield quote_data
#
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page:
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
#
#     def parse_author(self, response):
#         author_name = response.css('h3.author-title::text').get()
#         author_birthdate = response.css('span.author-born-date::text').get()
#         author_birthplace = response.css('span.author-born-location::text').get()
#         author_description = response.css('div.author-description::text').get()
#
#         # Usuń znaki nowej linii z pola "description"
#         author_description = author_description.replace('\n', '')
#
#         author_data = {
#             'fullname': author_name,
#             'born_date': author_birthdate,
#             'born_location': author_birthplace,
#             'description': author_description,
#         }
#
#         self.authors.append(author_data)
#         yield author_data
#
#     def closed(self, reason):
#         # Po zakończeniu parsowania, zapisz dane do plików JSON
#         with open('authors.json', 'w', encoding='utf-8') as f_authors:
#             json.dump(self.authors, f_authors, ensure_ascii=False, indent=4)
#
#         with open('quotes.json', 'w', encoding='utf-8') as f_quotes:
#             json.dump(self.quotes, f_quotes, ensure_ascii=False, indent=4)

# search by HTML
import scrapy
import json


class ScrapperSpider(scrapy.Spider):
    name = "scrapper"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(ScrapperSpider, self).__init__(*args, **kwargs)
        self.authors = []
        self.quotes = []

    def parse(self, response):
        for author_link in response.xpath('//small[@class="author"]/following-sibling::a/@href').extract():
            yield scrapy.Request(response.urljoin(author_link), callback=self.parse_author)

        for quote in response.xpath('//div[@class="quote"]'):
            quote_text = quote.xpath('span[@class="text"]/text()').get()
            quote_author = quote.xpath('span/small[@class="author"]/text()').get()

            quote_data = {
                'text': quote_text,
                'author': quote_author,
            }

            self.quotes.append(quote_data)
            yield quote_data

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_author(self, response):
        author_name = response.xpath('//h3[@class="author-title"]/text()').get()
        author_birthdate = response.xpath('//span[@class="author-born-date"]/text()').get()
        author_birthplace = response.xpath('//span[@class="author-born-location"]/text()').get()
        author_description = response.xpath('//div[@class="author-description"]/text()').get()

        # Usuń znaki nowej linii z pola "description"
        author_description = author_description.replace('\n', '')

        author_data = {
            'fullname': author_name,
            'born_date': author_birthdate,
            'born_location': author_birthplace,
            'description': author_description,
        }

        self.authors.append(author_data)
        yield author_data

    def closed(self, reason):
        # Po zakończeniu parsowania, zapisz dane do plików JSON
        with open('authors.json', 'w', encoding='utf-8') as f_authors:
            json.dump(self.authors, f_authors, ensure_ascii=False, indent=4)

        with open('quotes.json', 'w', encoding='utf-8') as f_quotes:
            json.dump(self.quotes, f_quotes, ensure_ascii=False, indent=4)
