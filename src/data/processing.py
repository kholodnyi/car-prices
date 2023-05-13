import argparse
import re
import urllib
from urllib.parse import unquote
from datetime import datetime
from typing import Union

from sqlalchemy.orm import Session
from tqdm import tqdm

from data.db import SessionLocal, _init_db
from data.models import CarListing, CleanedCarListing, CarMaker, CarModel, City, Province
from data.utils import OPTIONS_COLUMNS_SET


class CarListingCleaner:
    """
    Class for creating cleaned car listings from raw car listings.
    """

    def __init__(self, db_session: Session, batch_size: int = 100):
        self.db_session = db_session
        self.batch_size = batch_size
        self.CANT_BE_NULL_ATTRS = [
            'listing_url',
            'body_type',
            'carfax_no_accidents',
            'carfax_one_owner',
            'doors',
            'drivetrain',
            'body_type',
            'price',
            'kms',
            'is_new',
            'is_private',
            'make',
            'model',
            'num_photos',
            'year',
        ]
        self.DRIVETRAIN_MAP = {
            "AWD": "4WD",
            "4x4": "4WD",
            "4WD": "4WD",
            "FWD": "2WD",
            "RWD": "2WD",
            "2WD": "2WD",
            "4X4": "4WD",
        }

    @staticmethod
    def _parse_engine_data(engine_data: str) -> (float, int):
        engine_volume = None
        num_cylinders = None

        # regex pattern to match the engine volume and number of cylinders
        pattern = r'(\d+(\.\d+)?)\s*[Ll]\s*([a-zA-Z\-]+)?\s*(\d+)?\s*[Cc][yY][lL]'

        # search for a match in the engine data string
        match = re.search(pattern, engine_data)

        if match:
            engine_volume = float(match.group(1))
            if match.group(4):
                num_cylinders = int(match.group(4))
            else:
                # if the number of cylinders isn't specified, try to infer it from the engine description
                engine_description = match.group(3)
                if engine_description:
                    if "3" in engine_description:
                        num_cylinders = 3
                    if "4" in engine_description:
                        num_cylinders = 4
                    elif "6" in engine_description:
                        num_cylinders = 6
                    elif "8" in engine_description:
                        num_cylinders = 8
                    elif "10" in engine_description:
                        num_cylinders = 10
                    elif "12" in engine_description:
                        num_cylinders = 12

        return engine_volume, num_cylinders

    @staticmethod
    def _opt_name_transform(option: str):
        opt_name = option.lower().replace(' ', '_').replace('-', '_').replace(
            '/', '_').replace('(', '').replace(')', '').replace('&', '_')
        opt_name = opt_name.replace('___', '_')
        return f'opt_{opt_name}'

    @staticmethod
    def _define_fuel_type(raw_fuel_type: str) -> Union[str, None]:
        raw_fuel_type = raw_fuel_type.lower()
        if 'gas' in raw_fuel_type or 'unleaded' in raw_fuel_type:
            return 'Gasoline'
        elif 'diesel' in raw_fuel_type:
            return 'Diesel'
        elif 'hybrid' in raw_fuel_type:
            return 'Hybrid'
        elif 'flexible' in raw_fuel_type:
            return 'Flexible'
        else:
            return None

    @staticmethod
    def _define_cylinder_grouped(cylinder: int):
        if not isinstance(cylinder, int):
            raise TypeError(f'Invalid type for cylinder: {type(cylinder)}')
        if cylinder == 0:
            cylinder_grouped = '0'
        elif cylinder < 4:
            cylinder_grouped = 'less4'
        elif cylinder == 4:
            cylinder_grouped = '4'
        elif cylinder == 5:
            cylinder_grouped = '5'
        elif cylinder == 6:
            cylinder_grouped = '6'
        elif cylinder == 8:
            cylinder_grouped = '8'
        elif cylinder >= 10:
            cylinder_grouped = '10+'
        else:
            raise ValueError(f'Invalid cylinder value: {cylinder}')
        return cylinder_grouped

    @staticmethod
    def _define_city_province(listing_url: str) -> (str, str):
        # Parse the URL and extract the path
        parsed_url = urllib.parse.urlparse(listing_url)
        path = parsed_url.path

        # Split the path into its components
        path_components = path.split("/")

        # Get the city and province from the path components
        city = unquote(path_components[4])
        province = unquote(path_components[5])

        # Return the city and province as a tuple
        return city.title(), province.title()

    def create_cleaned_car_listings(self) -> (int, int):
        # get a batch of car listings that don't have a corresponding cleaned car listing
        car_listings = self.db_session.query(CarListing).outerjoin(CleanedCarListing).filter(
            CleanedCarListing.id == None,
            CarListing.bad_data == False,
        ).limit(self.batch_size).all()

        successful_cleaned_listings = 0

        for car_listing in car_listings:
            # transform and clean the car listing
            try:
                cleaned_listing = self._clean_car_listing(car_listing)
                # add the cleaned listing to the session
                self.db_session.add(cleaned_listing)
                successful_cleaned_listings += 1
                print('+', end='')
            except Exception as e:
                # print(f'Unable to clean car listing: {car_listing.listing_id}, error: {e}')
                print('-', end='')
                car_listing.bad_data = True

        # commit the session to save the new cleaned car listings to the database
        self.db_session.commit()
        return len(car_listings), successful_cleaned_listings

    def _clean_car_listing(self, car_listing: CarListing) -> CleanedCarListing:
        """
        Clean a single car listing.

        :param car_listing: CarListing object to clean.
        :return: CleanedCarListing object.
        """
        for attr in self.CANT_BE_NULL_ATTRS:
            if getattr(car_listing, attr) is None:
                raise Exception(f'Car listing does not have a {attr}.')

        cleaned_data = dict()

        # get city and province from the listing url
        cleaned_data['city'], cleaned_data['province'] = self._define_city_province(car_listing.listing_url)

        if car_listing.engine is None:
            if car_listing.make in ['Tesla', 'Rivian', 'Polestar', 'Lucid']:
                cleaned_data['engine'] = 'Electric'
            else:
                raise Exception('Car listing does not have an engine.')
        else:
            cleaned_data['engine'] = car_listing.engine

        if car_listing.transmission is None:
            if cleaned_data['engine'] == 'Electric':
                cleaned_data['transmission'] = 'Automatic'
            else:
                raise Exception('Car listing does not have a transmission.')
        else:
            if 'manual' in car_listing.transmission.lower():
                cleaned_data['transmission'] = 'Manual'
            else:
                cleaned_data['transmission'] = 'Automatic'

        if car_listing.fuel_type is None:
            if cleaned_data['engine'] == 'Electric':
                cleaned_data['fuel_type'] = 'Electric'
            else:
                raise Exception('Car listing does not have a fuel type.')
        else:
            if cleaned_data['engine'] == 'Electric':
                cleaned_data['fuel_type'] = 'Electric'
            else:
                fuel_type = self._define_fuel_type(car_listing.fuel_type)
                if fuel_type is None:
                    raise Exception('Car listing have undefined fuel type.')
                cleaned_data['fuel_type'] = fuel_type

        if car_listing.fuel_city is None or car_listing.fuel_combined is None or car_listing.fuel_highway is None:
            if cleaned_data['engine'] == 'Electric':
                cleaned_data['fuel_city'] = 0
                cleaned_data['fuel_combined'] = 0
                cleaned_data['fuel_highway'] = 0
            else:
                # save None values for now, would be updated later
                cleaned_data['fuel_city'] = None
                cleaned_data['fuel_combined'] = None
                cleaned_data['fuel_highway'] = None

        # filling engine volume and number of cylinders
        if cleaned_data['engine'] == 'Electric':
            cleaned_data['engine_volume'] = 0
            cleaned_data['cylinder'] = 0
        else:
            engine_volume, num_cylinders = self._parse_engine_data(car_listing.engine)
            cleaned_data['engine_volume'] = engine_volume
            if car_listing.cylinder is None:
                cleaned_data['cylinder'] = num_cylinders
            else:
                cleaned_data['cylinder'] = car_listing.cylinder

        cleaned_data['cylinder_grouped'] = self._define_cylinder_grouped(cleaned_data['cylinder'])

        # set drivetrain (can't be null)
        if car_listing.drivetrain.upper() in self.DRIVETRAIN_MAP:
            cleaned_data['drivetrain'] = self.DRIVETRAIN_MAP[car_listing.drivetrain.upper()]

        desc_keywords = ['description_premium', 'description_luxury', 'description_rebuild', 'description_sport']
        if car_listing.description is None:
            cleaned_data['description_len'] = 0
            for keyword in desc_keywords:
                cleaned_data[keyword] = 0
        else:
            cleaned_data['description_len'] = len(car_listing.description) if len(car_listing.description) < 2000 else 2000
            for keyword in desc_keywords:
                cleaned_data[keyword] = int(keyword in car_listing.description.lower())

        # verify that the car listing has a valid year
        if car_listing.year < 1985 or car_listing.year > datetime.now().year + 1:
            raise Exception(f'Car listing has an invalid year: {car_listing.year}')

        if car_listing.options is None or not car_listing.options:
            cleaned_data['options_qty'] = 0
            # raise Exception('Car listing does not have options.')
        else:
            cleaned_data['options_qty'] = len(car_listing.options)
            for raw_option in car_listing.options:
                option_name = self._opt_name_transform(raw_option)
                if option_name in OPTIONS_COLUMNS_SET:
                    cleaned_data[option_name] = 1

        del cleaned_data['engine']

        # also we don't use 'status' since it's duplicated with 'is_new'

        return CleanedCarListing(
            listing_url=car_listing.listing_url,
            _avg_market_price=car_listing._avg_market_price,
            car_listing=car_listing,
            body_type=car_listing.body_type,
            carfax_no_accidents=car_listing.carfax_no_accidents,
            carfax_one_owner=car_listing.carfax_one_owner,
            doors=car_listing.doors,
            price=car_listing.price,
            kms=car_listing.kms,
            is_new=car_listing.is_new,
            is_private=car_listing.is_private,
            make=car_listing.make,
            model=car_listing.model,
            num_photos=car_listing.num_photos,
            year=car_listing.year,
            **cleaned_data)

    def fill_makers_and_models(self):
        """Fill CarModel and corresponding CarMaker tables with data from CarListing table."""
        # select only distinct models and fetch only columns that we need
        car_listings = self.db_session.query(
            CarListing.make,
            CarListing.model
        ).distinct(CarListing.model).all()

        print(f'Found {len(car_listings)} distinct car models.')

        # car_listings = self.db_session.query(CarListing).all()
        car_makers = dict()
        car_models = dict()
        for car_listing in tqdm(car_listings):
            if car_listing.make not in car_makers.keys():
                car_maker = CarMaker(name=car_listing.make)
                car_makers[car_listing.make] = car_maker
                self.db_session.add(car_maker)
            else:
                car_maker = car_makers[car_listing.make]

            if car_listing.model not in car_models.keys():
                car_model = CarModel(name=car_listing.model, maker=car_maker)
                car_models[car_listing.model] = car_model
                self.db_session.add(car_model)

        self.db_session.commit()

    def fill_provinces_and_cities(self):
        """Fill Province and corresponding City tables with data from CarListing table."""
        # select only distinct models and fetch only columns that we need
        car_listings = self.db_session.query(
            CleanedCarListing.province,
            CleanedCarListing.city
        ).distinct(CleanedCarListing.city).all()

        print(f'Found {len(car_listings)} distinct cities.')

        # car_listings = self.db_session.query(CarListing).all()
        provinces = dict()
        cities = dict()
        for car_listing in tqdm(car_listings):
            if car_listing.province not in provinces.keys():
                province = Province(name=car_listing.province)
                provinces[car_listing.province] = province
                self.db_session.add(province)
            else:
                province = provinces[car_listing.province]

            if car_listing.city not in cities.keys():
                city = City(name=car_listing.city, province=province)
                cities[car_listing.city] = city
                self.db_session.add(city)

        self.db_session.commit()

    def clean_all_listings(self):
        total_successful = 0
        total_listings = 0

        current_listings = 1

        counter = 0

        while current_listings:
            current_listings, successful = self.create_cleaned_car_listings()
            total_successful += successful
            total_listings += current_listings
            print('\n', end='')

            # print progress each 10th iteration
            counter += 1
            if counter % 10 == 0:
                print(f'\nTotal listing: {total_listings} Total successful: {total_successful}')


def main(batch_size, mode):
    session = SessionLocal()

    mode = 'fill'
    print(f'Running cleaner in {mode} mode with batch size {batch_size}.')

    try:
        cleaner = CarListingCleaner(session, batch_size=batch_size)
        if mode == 'clean':
            cleaner.clean_all_listings()
        elif mode == 'fill':
            cleaner.fill_makers_and_models()
            cleaner.fill_provinces_and_cities()
        elif mode == 'all':
            # first fill table with cleaned listings
            cleaner.clean_all_listings()
            # and then based on that
            # fill makers and models, provinces and cities
            cleaner.fill_makers_and_models()
            cleaner.fill_provinces_and_cities()
        else:
            raise Exception(f'Unknown mode: {mode}')
    finally:
        session.close()


if __name__ == '__main__':
    _init_db()

    # define arguments for the script
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='Number of rows to process at a time.'
    )
    parser.add_argument(
        '--mode',
        type=str,
        default='clean',
        help='Mode to run the script in. Can be one of: clean, fill, all'
    )
    args = parser.parse_args()

    main(args.batch_size, args.mode)
