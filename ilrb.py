
import scrapy
import camelot
import tempfile
import logging


logging.getLogger("pdfminer").setLevel(logging.WARNING)
logging.getLogger("camelot").setLevel(logging.WARNING)

class ILRBSpider(scrapy.Spider):
    name = 'ilrbspider'
    start_urls = ['https://www2.illinois.gov/ilrb/decisions/bargainingcertifications/Pages/default.aspx']

    def parse(self, response):
        for yearly_certification_pdf_link in response.xpath('//div[@id="ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"]//ul/li/a'):
            yield response.follow(yearly_certification_pdf_link,
                                  self.parse_pdf)
    
    def parse_pdf(self, response):
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf') as tf:
            tf.write(response.body)
            tf.flush()
            flavor = 'lattice'
            tables = camelot.read_pdf(tf.name, flavor=flavor, pages='all')
            if not tables:
                flavor = 'stream'
                tables = camelot.read_pdf(tf.name,
                                          flavor=flavor,
                                          pages='all',
                                          row_tol=35)
                
        for i, table in enumerate(tables):
            for j, row in enumerate(table.data):
                yield {'data': row,
                       'source': response.url,
                       'table_num': i,
                       'row_num': j,
                       'flavor': flavor,
                       'camelot_accuracy': table.accuracy}
            
            
