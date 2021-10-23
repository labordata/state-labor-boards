
import scrapy
import camelot

class ILRBSpider(scrapy.Spider):
    name = 'ilrbspider'
    start_urls = ['https://www2.illinois.gov/ilrb/decisions/bargainingcertifications/Pages/default.aspx']

    def parse(self, response):
        for yearly_certification_pdf_link in response.xpath('//div[@id="ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"]//ul/li/a/@href').getall():
            tables = camelot.read_pdf(response.urljoin(yearly_certification_pdf_link), pages='all')
            first_table = tables[0].data
            header = [field.strip() for field in first_table[0]]
            for row in first_table[1:]:
                yield dict(zip(header, row))
            for table in tables[1:]:
                for row in table.data:
                    yield dict(zip(header, row))
