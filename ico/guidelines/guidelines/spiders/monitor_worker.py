import scrapy


class MonitorWorkerSpider(scrapy.Spider):
    name = "monitor_worker"
    allowed_domains = ["ico.org.uk"]
    #start_urls = ["https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/data-protection-and-monitoring-workers/"]
    start_urls = ["https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/"]

    def parse(self, response):
        yield {
            'section': response.css('#multipage-heading::text').get(),
            'url': response.url,
            'content': response.css('div.article-content').get(),
        }

        relative_reference = response.css('a.button.button-next.button-right').attrib['href']
        if relative_reference is not None:
            next_page = 'https://ico.org.uk' + relative_reference
            yield response.follow(next_page, callback = self.parse)