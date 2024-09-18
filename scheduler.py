import requests

def schedule_spider(property_type, payment_type):
    scrapyd_url = 'http://localhost:6800/schedule.json'
    project_name = 'scrapy_kafka_project'
    spider_name = 'property_spider'  # Replace this with your spider's name

    data = {
        'project': project_name,
        'spider': spider_name,
        'property_type': property_type,
        'payment_type': payment_type
    }

    response = requests.post(scrapyd_url, data=data)
    
    if response.status_code == 200:
        print(f"Spider scheduled successfully: {response.json()}")
    else:
        print(f"Failed to schedule spider: {response.content}")

# Schedule the spider with additional parameters
schedule_spider('flats-apartments', 'rent')
