from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapper import ScrapperSpider


def run_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ScrapperSpider)
    process.start()


if __name__ == "__main__":
    run_scraper()
