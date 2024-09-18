import scrapy
from kafka import KafkaProducer
import json

class PropertySpider(scrapy.Spider):
    name = "property_spider"
    base_url = 'https://buyrentkenya.com'  

    def __init__(self, property_type=None, payment_type=None, *args, **kwargs):
        super(PropertySpider, self).__init__(*args, **kwargs)
        self.property_type = property_type
        self.payment_type = payment_type
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',  # Change this if your Kafka server is not local
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def start_requests(self):
        if self.property_type and self.payment_type:
            for page in range(1, 6):  # Adjust the range as needed
                if page == 1:
                    url = f'{self.base_url}/{self.property_type}-for-{self.payment_type}'
                else:
                    url = f'{self.base_url}/{self.property_type}-for-{self.payment_type}?page={page}'
                    yield scrapy.Request(url=url, callback=self.parse_page, meta={'property_type': self.property_type, 'payment_type': self.payment_type})
        else:
            self.logger.error('Property type and payment type must be provided.')
    def parse_page(self, response):
        houses = response.css('div.flex.flex-col.justify-between.px-5.py-4.md\\:w-3\\/5')
        
        for house in houses:
            try:
                url = house.css('h2.font-semibold.md\\:hidden a.no-underline::attr(href)').get()
                if url:
                    house_url = self.base_url + url
                    request = scrapy.Request(house_url, callback=self.parse_house)
                    request.meta['property_type'] = response.meta['property_type']
                    request.meta['payment_type'] = response.meta['payment_type']
                    yield request
            except Exception as e:
                self.logger.error(f"Error processing house: {e}")

    def parse_house(self, response):
        try:
            property_type = response.meta['property_type']
            payment_type = response.meta['payment_type']

            title = response.css('h1.hidden.text-lg.font-semibold.sm\\:hidden.md\\:block.md\\:text-2xl::text').get()
            location = response.css('p.hidden.items-center.text-sm.text-gray-500.md\\:flex::text').get()
            bedrooms = ''.join(response.css('span[aria-label="bedrooms"]::text').getall()).strip()
            bathrooms = ''.join(response.css('span[aria-label="bathrooms"]::text').getall()).strip()
            size = response.css('span[aria-label="area"]::text').get()
            date = response.css('div.flex.justify-between.py-2 span.font-semibold::text').get()

            amenities = []
            # Extract features from each category
            sections = response.css('div[data-cy="listing-amenities-component"] div.flex.flex-col')
            for section in sections:
                # Extract features for the current section
                features = section.css('ul.flex li div::text').getall()
                amenities.extend([feature.strip() for feature in features if feature.strip()])            # cleaned_amenities = [amenity.strip() for amenity in amenities if amenity.strip()]
            
            price = response.css('span.block.text-right.text-xl.font-semibold.leading-7.md\\:text-xxl.md\\:font-extrabold::text').get()
            
            data = {
                "Title": title.strip() if title else None,
                "Location": location.strip() if location else None,
                "Bedrooms": bedrooms.strip() if bedrooms else None,
                "Bathrooms": bathrooms.strip() if bathrooms else None,
                "Size": size.strip() if size else None,
                "Date": date.strip() if date else None,
                "Amenities": [amenity.strip() for amenity in amenities],
                "Url": response.url,
                "Property Type": property_type,
                "Payment_type": payment_type,
                "Price": price.strip() if price else None
            }

            self.producer.send('property_topic', data)
            self.producer.flush()
            yield data  # Yield the scraped data
        except Exception as e:
            self.logger.error(f"Error parsing house details: {e}")
