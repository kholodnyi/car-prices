import joblib
import pandas as pd

from .models import CarMaker, CarModel, Province, City, MachineLearningModel

import sys
import os

# Add the path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

from data.processing import CarListingCleaner
from data.utils import apply_column_mapping, ONE_HOT_ENCODE_COLUMNS


def transform_from_input(form_data, post_data):
    """Transforms input data to a dictionary ready to be used by the model."""
    data = {}
    data.update(form_data)

    data['make'] = CarMaker.objects.get(id=post_data.get('car_maker')).name
    data['model'] = CarModel.objects.get(id=post_data.get('car_model')).name
    data['province'] = Province.objects.get(id=post_data.get('province')).name
    data['city'] = City.objects.get(id=post_data.get('city')).name

    data['cylinder_grouped'] = CarListingCleaner._define_cylinder_grouped(data['cylinder'])
    del data['cylinder']

    data['age'] = 2025 - data['year']  # some new cars are listed as 2024 (avoiding zero division)
    data['mileage_per_year'] = data['kms'] / data['age']  # how much kms was driven per year

    # count the number of options
    # by counting the number keys that start with 'opt_'
    # and have true as value
    data['options_qty'] = len([key for key, value in data.items() if key.startswith('opt_') and value is True])

    input_df = pd.DataFrame([data])

    input_df = apply_column_mapping(input_df)

    # Drop the original categorical columns
    input_df.drop(columns=ONE_HOT_ENCODE_COLUMNS, inplace=True)

    input_df = input_df.sort_index(axis=1)

    # fix some features names
    renamed = {}
    for col in input_df.columns:
        renamed[col] = col.replace('<', '').replace(',', '_')
    input_df.rename(columns=renamed, inplace=True)

    return input_df


def make_prediction(df: pd.DataFrame) -> str:
    predictions = {'linear': None, 'boosting': None}
    for model_name in ['linear', 'boosting']:
        # Load the model most recent model (updated_at)
        model_path_raw = MachineLearningModel.objects.filter(
            name=model_name
        ).latest(
            'updated_at'
        ).model_file.path
        model_path = os.path.join(os.path.dirname(__file__), model_path_raw)
        model = joblib.load(model_path)

        predictions[model_name] = model.predict(df)[0]

    # form prediction string
    prediction = f'Prediction (Boosting): {predictions["boosting"]:,.2f} CAD<br>' \
                 f'Prediction (Linear):   {predictions["linear"]:,.2f} CAD<br>'
    return prediction
