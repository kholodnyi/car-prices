from typing import List

import pandas as pd
from sqlalchemy import func

from data.db import SessionLocal
from data.models import CleanedCarListing
from data.utils import apply_column_mapping, ONE_HOT_ENCODE_COLUMNS


def get_all_listings(price_from: int = 5000, price_to: int = 130000, only: str = None) -> List[CleanedCarListing]:
    if price_from >= price_to:
        raise ValueError('price_from must be less than price_to')

    session = SessionLocal()
    # filter listings by price range
    query = session.query(CleanedCarListing).filter(
        CleanedCarListing.price >= price_from,
        CleanedCarListing.price <= price_to,
    )

    # exclude cars with high mileage
    # almost all of them are mistakes
    query = query.filter(CleanedCarListing.kms <= 500000)

    # exclude listings which model is represented less than 150 times
    # this is to exclude rare models
    popular_models = session.query(
        CleanedCarListing.model,
    ).group_by(
        CleanedCarListing.model,
    ).having(
        func.count(CleanedCarListing.model) >= 150,
    ).subquery()
    query = query.join(
        popular_models,
        CleanedCarListing.model == popular_models.c.model,
    )

    # exclude listings which are older than 1980
    # this is to exclude rare models
    query = query.filter(CleanedCarListing.year >= 1985)

    # exclude listings which have kms less than 1000 and price under 20000
    # this is to exclude mistakes
    query = query.filter(
        ~((CleanedCarListing.kms < 1000) & (CleanedCarListing.price < 20000))
    )

    # if only == 'EV':
    #     # exclude listings which are not EVs
    #     query = query.filter(CleanedCarListing.fuel_type == 'Electric')
    # elif only == 'ICE':
    #     # exclude listings which are EVs
    #     query = query.filter(CleanedCarListing.fuel_type != 'Electric')

    listings = query.all()
    session.close()
    return listings


def get_listings_df(exclude_options: bool = True, only: str = None) -> pd.DataFrame:
    listings = get_all_listings(only=only)
    df = pd.DataFrame([listing.as_dict() for listing in listings])

    # drop unwanted columns
    drop_cols = [
        'id',
        '_avg_market_price',   # price prediction from car listing websites
        'engine_volume',       # a lot of missing values
        'listing_url',         # not useful for ml
        'car_listing_id',      # fk to car_listing table
        'cylinder',            # this is a duplicate of cylinder_grouped
    ]

    # a lot of missing values
    drop_cols += [col for col in df.columns if col.startswith('fuel_') and col != 'fuel_type']

    if exclude_options:
        # add all opt columns to drop_cols
        drop_cols += [col for col in df.columns if col.startswith('opt_')]

    df = df.drop(columns=drop_cols)

    # additional feature engineering
    df['age'] = 2025 - df['year']  # some new cars are listed as 2024 (avoiding zero division)
    df['mileage_per_year'] = df['kms'] / df['age']  # how much kms was driven per year

    return df


def get_single_listing_df(cleaned_listing: CleanedCarListing) -> pd.DataFrame:
    df = pd.DataFrame([cleaned_listing.as_dict()])

    df = process_df(df, exclude_options=False)

    # fill missing values with zeros only for opt_ columns
    for col in df.columns:
        if col.startswith('opt_'):
            df[col].fillna(0, inplace=True)

    return df


def process_df(df: pd.DataFrame, exclude_options: bool = True):
    # drop unwanted columns
    drop_cols = [
        'id',
        '_avg_market_price',   # price prediction from car listing websites
        'engine_volume',       # a lot of missing values
        'listing_url',         # not useful for ml
        'car_listing_id',      # fk to car_listing table
        'cylinder',            # this is a duplicate of cylinder_grouped
    ]

    # a lot of missing values
    drop_cols += [col for col in df.columns if col.startswith('fuel_') and col != 'fuel_type']

    if exclude_options:
        # add all opt columns to drop_cols
        drop_cols += [col for col in df.columns if col.startswith('opt_')]

    df = df.drop(columns=drop_cols)

    # additional feature engineering
    df['age'] = 2025 - df['year']  # some new cars are listed as 2024 (avoiding zero division)
    df['mileage_per_year'] = df['kms'] / df['age']  # how much kms was driven per year

    df = apply_column_mapping(df)

    # Drop the original categorical columns
    df.drop(columns=ONE_HOT_ENCODE_COLUMNS, inplace=True)

    df = df.sort_index(axis=1)

    df.drop(columns=['price'], inplace=True)

    # fix some features names
    renamed = {}
    for col in df.columns:
        renamed[col] = col.replace('<', '').replace(',', '_')
    df.rename(columns=renamed, inplace=True)

    return df
