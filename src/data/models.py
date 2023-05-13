import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from data.db import CustomBase


class CarListing(CustomBase):
    """
    Representation of a cryptocurrency ticker.
    """
    __tablename__ = "cars_ml_listing"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, unique=True)
    listing_url = Column(String)  #
    _avg_market_price = Column(String)  #
    body_type = Column(String)  #
    carfax_no_accidents = Column(Integer)  #
    carfax_one_owner = Column(Integer)  #
    cylinder = Column(Integer)  #
    description = Column(String)  #
    doors = Column(Integer)  #
    drivetrain = Column(String)  #
    engine = Column(String)  #
    fuel_city = Column(Float)  #
    fuel_combined = Column(Float)  #
    fuel_highway = Column(Float)  #
    fuel_type = Column(String)  #
    is_new = Column(Integer)  #
    is_private = Column(Integer)  #
    kms = Column(Integer)  #
    make = Column(String)  #
    model = Column(String)  #
    num_photos = Column(Integer)  #
    options = Column(JSON)
    price = Column(Integer)  #
    status = Column(String)  #
    transmission = Column(String)  #
    year = Column(Integer)  #
    bad_data = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CleanedCarListing(CustomBase):
    """
    Representation of a cleaned and processed car listing.
    """
    __tablename__ = "cleaned_cars_ml_listing"

    id = Column(Integer, primary_key=True)
    car_listing_id = Column(Integer, ForeignKey('cars_ml_listing.id'), unique=True)
    car_listing = relationship("CarListing", backref="cleaned_car_listing")

    # columns from cars_ml_listing as is, no need to clean
    listing_url = Column(String)
    _avg_market_price = Column(String)

    city = Column(String)  #
    province = Column(String)  #
    body_type = Column(String)  #
    carfax_no_accidents = Column(Integer)  # boolean
    carfax_one_owner = Column(Integer)  # boolean
    doors = Column(Integer)  #
    drivetrain = Column(String)
    engine_volume = Column(Float)  #
    fuel_city = Column(Float)  #
    fuel_combined = Column(Float)  #
    fuel_highway = Column(Float)  #
    fuel_type = Column(String)  #
    cylinder = Column(Integer)  #
    cylinder_grouped = Column(String)  #
    price = Column(Integer)  #
    is_new = Column(Integer)  #
    is_private = Column(Integer)  #
    kms = Column(Integer)  #
    make = Column(String)  #
    model = Column(String)  #
    num_photos = Column(Integer)  #
    transmission = Column(String)  #
    year = Column(Integer)  #

    description_len = Column(Integer)  #
    description_premium = Column(Integer)  # boolean
    description_luxury = Column(Integer)  # boolean
    description_rebuild = Column(Integer)  # boolean
    description_sport = Column(Integer)  # boolean

    options_qty = Column(Integer)  #

    # # options
    opt_heated_steering_wheel = Column(Integer, default=0)
    opt_auto_on_off_headlamps = Column(Integer, default=0)
    opt_illuminated_visor_mirror = Column(Integer, default=0)
    opt_dual_climate_controls = Column(Integer, default=0)
    opt_satellite_radio = Column(Integer, default=0)
    opt_power_brakes = Column(Integer, default=0)
    opt_anti_theft = Column(Integer, default=0)
    opt_driver_side_airbag = Column(Integer, default=0)
    opt_all_wheel_drive = Column(Integer, default=0)
    opt_memory_seats = Column(Integer, default=0)
    opt_daytime_running_lights = Column(Integer, default=0)
    opt_cd_player = Column(Integer, default=0)
    opt_power_locks = Column(Integer, default=0)
    opt_auxiliary_12v_outlet = Column(Integer, default=0)
    opt_remote_starter = Column(Integer, default=0)
    opt_heated_seats = Column(Integer, default=0)
    opt_rear_defroster = Column(Integer, default=0)
    opt_intermittent_wipers = Column(Integer, default=0)
    opt_power_windows = Column(Integer, default=0)
    opt_privacy_glass = Column(Integer, default=0)
    opt_power_seat = Column(Integer, default=0)
    opt_roll_bar = Column(Integer, default=0)
    opt_steering_wheel_audio_controls = Column(Integer, default=0)
    opt_child_safety_locks = Column(Integer, default=0)
    opt_cruise_control = Column(Integer, default=0)
    opt_sunroof = Column(Integer, default=0)
    opt_telescoping_steering = Column(Integer, default=0)
    opt_power_lift_gates = Column(Integer, default=0)
    opt_bluetooth = Column(Integer, default=0)
    opt_cup_holder = Column(Integer, default=0)
    opt_alloy_wheels = Column(Integer, default=0)
    opt_anti_lock_brakes_abs = Column(Integer, default=0)
    opt_leather_wrap_wheel = Column(Integer, default=0)
    opt_trip_odometer = Column(Integer, default=0)
    opt_reverse_parking_sensors = Column(Integer, default=0)
    opt_air_conditioning = Column(Integer, default=0)
    opt_engine_8cyl = Column(Integer, default=0)
    opt_fog_lights = Column(Integer, default=0)
    opt_auto_dimming_mirrors = Column(Integer, default=0)
    opt_crew_cab = Column(Integer, default=0)
    opt_split_folding_rear_seats = Column(Integer, default=0)
    opt_security_system = Column(Integer, default=0)
    opt_fully_loaded = Column(Integer, default=0)
    opt_front_wheel_drive = Column(Integer, default=0)
    opt_6_speed = Column(Integer, default=0)
    opt_remote_trunk_release = Column(Integer, default=0)
    opt_rear_window_wiper = Column(Integer, default=0)
    opt_lane_departure_warning = Column(Integer, default=0)
    opt_stability_control = Column(Integer, default=0)
    opt_spoiler = Column(Integer, default=0)
    opt_power_steering = Column(Integer, default=0)
    opt_side_impact_airbag = Column(Integer, default=0)
    opt_am_fm_stereo = Column(Integer, default=0)
    opt_mp3_cd_player = Column(Integer, default=0)
    opt_adaptive_cruise_control = Column(Integer, default=0)
    opt_traction_control = Column(Integer, default=0)
    opt_digital_clock = Column(Integer, default=0)
    opt_premium_audio = Column(Integer, default=0)
    opt_tinted_windows = Column(Integer, default=0)
    opt_3rd_row_seating = Column(Integer, default=0)
    opt_remote_start = Column(Integer, default=0)
    opt_heated_mirrors = Column(Integer, default=0)
    opt_wood_trim_interior = Column(Integer, default=0)
    opt_anti_starter = Column(Integer, default=0)
    opt_power_adjustable_seat = Column(Integer, default=0)
    opt_xenon_headlights = Column(Integer, default=0)
    opt_panoramic_sunroof = Column(Integer, default=0)
    opt_leather_interior = Column(Integer, default=0)
    opt_navigation_system = Column(Integer, default=0)
    opt_tilt_steering = Column(Integer, default=0)
    opt_tachometer = Column(Integer, default=0)
    opt_tow_package = Column(Integer, default=0)
    opt_rear_view_camera = Column(Integer, default=0)
    opt_rear_air_heat = Column(Integer, default=0)
    opt_power_mirrors = Column(Integer, default=0)
    opt_rain_sensor_wipers = Column(Integer, default=0)
    opt_keyless_entry = Column(Integer, default=0)
    opt_bucket_seats = Column(Integer, default=0)
    opt_console = Column(Integer, default=0)
    opt_map_lights = Column(Integer, default=0)
    opt_climate_control = Column(Integer, default=0)
    opt_dual_airbag = Column(Integer, default=0)
    opt_trip_computer = Column(Integer, default=0)
    opt_cloth_interior = Column(Integer, default=0)
    opt_passenger_airbag = Column(Integer, default=0)


class CarMaker(CustomBase):
    __tablename__ = 'car_makers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    cars = relationship('CarModel', backref='maker', lazy='dynamic')

    def __repr__(self):
        return '<CarMaker %r>' % self.name


class CarModel(CustomBase):
    __tablename__ = 'car_models'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    maker_id = Column(Integer, ForeignKey('car_makers.id'), nullable=False)

    def __repr__(self):
        return '<CarModel %r>' % self.name


class Province(CustomBase):
    __tablename__ = 'provinces'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    cities = relationship('City', backref='province', lazy='dynamic')

    def __repr__(self):
        return '<Province %r>' % self.name


class City(CustomBase):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    province_id = Column(Integer, ForeignKey('provinces.id'), nullable=False)

    def __repr__(self):
        return '<City %r>' % self.name
