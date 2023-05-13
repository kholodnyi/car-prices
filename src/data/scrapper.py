import random
import time

import requests
from bs4 import BeautifulSoup

from config import settings
from data.db import SessionLocal, _init_db
from data.models import CarListing
from data.utils import headers, PROVINCES, URL_TEMPLATE, handle_script_text
from log import logger


class Scrapper:
    def __init__(
        self,
        province_to_parse: str = None,
        price_range: tuple = (2000, 180000),
    ):
        self.running = True
        self.db_session = SessionLocal()
        self.price_range = price_range

        self.province_to_parse = province_to_parse

    def run(self):
        if self.province_to_parse is None:
            provinces_to_parse = [name for name in PROVINCES.keys()]
        else:
            provinces_to_parse = [self.province_to_parse]
        logger.info(f'Parsing {provinces_to_parse}')
        for province in provinces_to_parse:
            cars_parsed = self.scrape_listings(
                min_price=self.price_range[0],
                max_price=self.price_range[1],
                province_name=PROVINCES[province]['name'],
                location=PROVINCES[province]['location'],
                code=PROVINCES[province]['code']
            )
            logger.info(f'Parsed {cars_parsed} cars in {province}')

    def scrape_listings(self, min_price, max_price, province_name, location, code):
        current_offset = 0
        cars = 0

        retry = 1

        while self.running:
            time.sleep(random.uniform(1, 2.4))
            url = URL_TEMPLATE.format(
                code=code,
                offset=current_offset,
                min_price=min_price,
                max_price=max_price,
                province_name=province_name,
                location=location)

            logger.info(f'fetching: {url}')
            try:
                response = requests.get(url, headers=headers)
                retry = 1
            except Exception as e:
                if retry > 4:
                    break
                time.sleep(retry ** 3 + random.uniform(1, 2))
                logger.error(f'Failed to fetch page: {e}')
                retry += 1
                continue

            if response.status_code != 200:
                logger.error(f'Failed to fetch page: {response.status_code}')
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('div', class_='listing-details')

            if not listings:
                break

            for listing in listings:
                time.sleep(random.uniform(1, 2.4))
                link = listing.find('a', class_='result-title click')['href']
                listing_url = f'https://www.autotrader.ca{link}'
                logger.info(f'scrapping: {listing_url}')

                response = requests.get(listing_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                script_tag = soup.find('script', string=lambda t: 'ngVdpModel' in str(t))

                if script_tag is not None:
                    script_text = script_tag.string.strip()

                    try:
                        car_data = handle_script_text(script_text)
                        car_data['listing_url'] = listing_url
                    except Exception as e:
                        logger.error(e)
                        continue

                    # Save to database in CarListing SQLAlchemy model
                    try:
                        car_listing = CarListing(**car_data)
                        self.db_session.add(car_listing)
                        self.db_session.commit()
                        cars += 1
                    except Exception as e:
                        logger.error(e)
                        self.db_session.rollback()

                else:
                    logger.error('Could not find script tag with ngVdpModel data.')

            current_offset += 100

        self.db_session.close()

        return cars

    def stop(self):
        self.running = False

    @staticmethod
    def scrape_one_listing(listing_url: str) -> dict:
        response = requests.get(listing_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        script_tag = soup.find('script', string=lambda t: 'ngVdpModel' in str(t))

        if script_tag is not None:
            script_text = script_tag.string.strip()

            try:
                car_data = handle_script_text(script_text)
                car_data['listing_url'] = listing_url
                return car_data
            except Exception as e:
                logger.error(e)
                return {'error': e}

        else:
            logger.error('Could not find script tag with ngVdpModel data.')
            return {'error': 'Could not find script tag with ngVdpModel data.'}


if __name__ == '__main__':
    _init_db()
    scrapper = Scrapper(province_to_parse=settings.PROVINCE)
    try:
        scrapper.run()
    except KeyboardInterrupt:
        print("Stopping scrapper...")
    finally:
        scrapper.stop()
