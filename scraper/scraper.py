import requests
from bs4 import BeautifulSoup
import pandas as pd
from kafka import KafkaProducer
import os
import time
import json
import logging

logging.basicConfig(level=logging.INFO)

shop_url = 'https://scrapeme.live/shop/'
topic_name = 'ml-engineer'

def get_product_information(url): # returns pokemon information of given url
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find('h1', class_='product_title')
        price = soup.find('p', class_='price')
        description_div = soup.find('div', class_='woocommerce-product-details__short-description')
        description = description_div.find('p')
        stock = soup.find('p', class_='stock')
        return {
            "name": name.get_text(strip=True),
            "price": price.get_text(strip=True),
            "description": description.get_text(strip=True),
            "stock": stock.get_text(strip=True)
        }
    else:
        logging.error(f"Failed to get product info. Status code: {response.status_code}")
        return None


def get_product_urls(url): # returns product urls of infividual pokemons
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_urls = []

        ul = soup.find('ul', class_='products')
        if ul:
            li_items = ul.find_all('li')
            for li in li_items:
                a_tag = li.find('a')
                if a_tag:
                    href_url = a_tag['href']
                    product_urls.append(href_url)
            return product_urls
        else:
            logging.error(f"Failed to find ul tag with class 'products' in page. Status code: {response.status_code}")
            return []

    
def produce_kafka_messages(producer, topic, data): # produces kafka messages for with given parameters in 1 seconds of interval
    with open('data.json', 'w', encoding='utf-8') as file:
        for record in data:
            try:
                future = producer.send(topic, record)
                result = future.get(timeout=20)
                logging.info(f"Message sent to topic {result.topic}, partition {result.partition}, offset {result.offset}")
                json.dump(record, file, ensure_ascii=False)
                file.write('\n')
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
            time.sleep(1) # this is what i understood from 1 seconds of interval
        producer.flush()

def main():
    product_urls = get_product_urls(shop_url)

    data = []
    for url in product_urls:
        info = get_product_information(url)
        if info:
            data.append(info)

    if data:
        df = pd.DataFrame(data)
        json_data = df.to_json(orient='records') # save the data into a json file
        data = json.loads(json_data)

        kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
           value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        produce_kafka_messages(producer, topic_name, data)
        producer.close()

    else:
        logging.error("No data to produce.")

if __name__ == "__main__":
    main()