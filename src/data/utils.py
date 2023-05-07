import json

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
