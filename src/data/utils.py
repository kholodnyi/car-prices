import json
import os

import pandas as pd

_SPECS_KEY_MAPPING = {
    'Kilometres': 'kms',
    'Status': 'status',
    'Body Type': 'body_type',
    'Engine': 'engine',
    'Cylinder': 'cylinder',
    'Transmission': 'transmission',
    'Drivetrain': 'drivetrain',
    'Doors': 'doors',
    'Fuel Type': 'fuel_type',
}
_SPECS_TO_INT = {
    'Kilometres',
    'Cylinder',
    'Doors',
}

# set of popular options (names of CleanCarOption columns)
OPTIONS_COLUMNS_SET = {
    'opt_heated_steering_wheel',
    'opt_auto_on_off_headlamps',
    'opt_illuminated_visor_mirror',
    'opt_dual_climate_controls',
    'opt_satellite_radio',
    'opt_power_brakes',
    'opt_anti_theft',
    'opt_driver_side_airbag',
    'opt_all_wheel_drive',
    'opt_memory_seats',
    'opt_daytime_running_lights',
    'opt_cd_player',
    'opt_power_locks',
    'opt_auxiliary_12v_outlet',
    'opt_remote_starter',
    'opt_heated_seats',
    'opt_rear_defroster',
    'opt_intermittent_wipers',
    'opt_power_windows',
    'opt_privacy_glass',
    'opt_power_seat',
    'opt_roll_bar',
    'opt_steering_wheel_audio_controls',
    'opt_child_safety_locks',
    'opt_cruise_control',
    'opt_sunroof',
    'opt_telescoping_steering',
    'opt_power_lift_gates',
    'opt_bluetooth',
    'opt_cup_holder',
    'opt_alloy_wheels',
    'opt_anti_lock_brakes_abs',
    'opt_leather_wrap_wheel',
    'opt_trip_odometer',
    'opt_reverse_parking_sensors',
    'opt_air_conditioning',
    'opt_engine_8cyl',
    'opt_fog_lights',
    'opt_auto_dimming_mirrors',
    'opt_crew_cab',
    'opt_split_folding_rear_seats',
    'opt_security_system',
    'opt_fully_loaded',
    'opt_front_wheel_drive',
    'opt_6_speed',
    'opt_remote_trunk_release',
    'opt_rear_window_wiper',
    'opt_lane_departure_warning',
    'opt_stability_control',
    'opt_spoiler',
    'opt_power_steering',
    'opt_side_impact_airbag',
    'opt_am_fm_stereo',
    'opt_mp3_cd_player',
    'opt_adaptive_cruise_control',
    'opt_traction_control',
    'opt_digital_clock',
    'opt_premium_audio',
    'opt_tinted_windows',
    'opt_3rd_row_seating',
    'opt_remote_start',
    'opt_heated_mirrors',
    'opt_wood_trim_interior',
    'opt_anti_starter',
    'opt_power_adjustable_seat',
    'opt_xenon_headlights',
    'opt_panoramic_sunroof',
    'opt_leather_interior',
    'opt_navigation_system',
    'opt_tilt_steering',
    'opt_tachometer',
    'opt_tow_package',
    'opt_rear_view_camera',
    'opt_rear_air___heat',
    'opt_power_mirrors',
    'opt_rain_sensor_wipers',
    'opt_keyless_entry',
    'opt_bucket_seats',
    'opt_console',
    'opt_map_lights',
    'opt_climate_control',
    'opt_dual_airbag',
    'opt_trip_computer',
    'opt_cloth_interior',
    'opt_passenger_airbag',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

URL_TEMPLATE = "https://www.autotrader.ca/cars/{code}/?rcp=100&rcs={offset}&pRng={min_price}%2C{max_price}&prx=-2&prv={province_name}&loc={location}&hprc=True&wcp=True"

PROVINCES = {
    'AB': {
        'name': 'Alberta',
        'location': 'Calgary',
        'code': 'ab',
    },
    'BC': {
        'name': 'British%20Columbia',
        'location': 'Vancouver',
        'code': 'bc',
    },
    'MB': {
        'name': 'Manitoba',
        'location': 'Winnipeg',
        'code': 'mb',
    },
    'NB': {
        'name': 'New%20Brunswick',
        'location': 'Fredericton',
        'code': 'nb',
    },
    'NL': {
        'name': 'Newfoundland%20and%20Labrador',
        'location': 'Cartwright',
        'code': 'nl',
    },
    'NT': {
        'name': 'Northwest%20Territories',
        'location': 'Yellowknife',
        'code': 'nt',
    },
    'NS': {
        'name': 'Nova%20Scotia',
        'location': 'Halifax',
        'code': 'ns',
    },
    'NU': {
        'name': 'Nunavut',
        'location': 'Iqaluit',
        'code': 'nu',
    },
    'ON': {
        'name': 'Ontario',
        'location': 'Toronto',
        'code': 'on',
    },
    'PE': {
        'name': 'Prince%20Edward%20Island',
        'location': 'Charlottetown',
        'code': 'pe',
    },
    'QC': {
        'name': 'Quebec',
        'location': 'Montreal',
        'code': 'qc',
    },
    'SK': {
        'name': 'Saskatchewan',
        'location': 'Regina',
        'code': 'sk',
    }
}

ONE_HOT_ENCODE_COLUMNS = [
    'body_type',
    'drivetrain',
    'fuel_type',
    'make',
    'model',
    'transmission',
    'city',
    'province',
    'cylinder_grouped',
]


def convert_str_to_int(string):
    """Converts a string like this: `1,234 km`, `$1,234` to an integer."""
    cleaned_str = ''.join([c for c in string if c.isdigit()])
    return int(cleaned_str)


def handle_script_text(script_text: str):
    raw_rows = script_text.split('\r\n')

    data_dict = None
    for raw_row in raw_rows[1:]:
        if raw_row.startswith('        window[\'ngVdpModel\'] = '):
            data_dict = json.loads('='.join(raw_row.strip().split('=')[1:])[:-1])
            break

    if data_dict is None:
        raise Exception('Could not find ngVdpModel data.')

    car_data = {}

    for spec in data_dict['specifications']['specs']:
        try:
            if spec['key'] in _SPECS_TO_INT:
                value = convert_str_to_int(spec['value'])
            else:
                value = spec['value']
            car_data[_SPECS_KEY_MAPPING[spec['key']]] = value
        except KeyError:
            pass

    car_data['listing_id'] = convert_str_to_int(data_dict['adBasicInfo']['adId'])

    car_data['price'] = convert_str_to_int(data_dict['adBasicInfo']['price'])
    car_data['status'] = data_dict['adBasicInfo']['status']
    car_data['make'] = data_dict['adBasicInfo']['make']
    car_data['model'] = data_dict['adBasicInfo']['model']
    car_data['year'] = int(data_dict['adBasicInfo']['year'])
    car_data['is_new'] = int(data_dict['adBasicInfo']['isNew'])
    car_data['is_private'] = 0 if 'dealerId' in data_dict else 1
    # car_data['body_type'] = data_dict['adBasicInfo']['splashBodyType']
    car_data['num_photos'] = data_dict['gallery']['count']

    try:
        car_data['fuel_city'] = float(data_dict['fuelEconomy']['fuelCity'])
        car_data['fuel_combined'] = float(data_dict['fuelEconomy']['fuelCity'])
        car_data['fuel_highway'] = float(data_dict['fuelEconomy']['fuelHighway'])
    except:
        car_data['fuel_city'] = None
        car_data['fuel_combined'] = None
        car_data['fuel_highway'] = None

    try:
        options = data_dict['featureHighlights']['options']
    except KeyError:
        options = []

    try:
        highlights = data_dict['featureHighlights']['highlights']
    except KeyError:
        highlights = []

    car_data['options'] = options + highlights

    try:
        car_data['_avg_market_price'] = convert_str_to_int(data_dict['priceAnalysis']['averageMarketPrice'])
    except:
        car_data['_avg_market_price'] = None

    try:
        car_data['description'] = data_dict['description']['description'][0]['description']
    except (KeyError, IndexError):
        car_data['description'] = None

    # carfax data
    try:
        car_fax_data = data_dict['carfax']
        car_data['carfax_one_owner'] = int(car_fax_data['showOneOwner'])
        car_data['carfax_no_accidents'] = int(car_fax_data['showReportedNoAccidents'])
    except KeyError:
        car_data['carfax_one_owner'] = 0
        car_data['carfax_no_accidents'] = 0

    return car_data


def apply_column_mapping(df: pd.DataFrame):
    # Load the column mappings from the file that located in the same directory as this script
    # and named column_mappings.json
    with open(os.path.join(os.path.dirname(__file__), 'column_mappings.json')) as f:
        column_mappings = json.load(f)

        # Apply the column mappings to the input DataFrame
    for column, encoded_columns in column_mappings.items():
        # Create new columns with the encoded values
        for encoded_column in encoded_columns:
            df[encoded_column] = 0

        # Set the value of the corresponding encoded column based on the input data
        value = df[column].iloc[0]
        encoded_column = f"{column}_{value}"
        if encoded_column in df.columns:
            df.at[0, encoded_column] = 1

    return df
