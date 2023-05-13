import json
import re
from typing import Any

from django.db import models


class RawJSONField(models.JSONField):
    def db_type(self, connection):
        return 'json'

    def get_prep_value(self, value):
        return value

    def from_db_value(self, value, expression, connection):
        return value


class CarListing(models.Model):
    """
    Representation of a cryptocurrency ticker.
    """
    listing_id = models.IntegerField(unique=True)
    listing_url = models.CharField(max_length=255)
    _avg_market_price = models.CharField(max_length=255)
    body_type = models.CharField(max_length=255)
    carfax_no_accidents = models.IntegerField()
    carfax_one_owner = models.IntegerField()
    cylinder = models.IntegerField()
    description = models.CharField(max_length=255)
    doors = models.IntegerField()
    drivetrain = models.CharField(max_length=255)
    engine = models.CharField(max_length=255)
    fuel_city = models.FloatField()
    fuel_combined = models.FloatField()
    fuel_highway = models.FloatField()
    fuel_type = models.CharField(max_length=255)
    is_new = models.IntegerField()
    is_private = models.IntegerField()
    kms = models.IntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    num_photos = models.IntegerField()
    options = RawJSONField()
    price = models.IntegerField()
    status = models.CharField(max_length=255)
    transmission = models.CharField(max_length=255)
    year = models.IntegerField()
    bad_data = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_options(self):
        try:
            return json.loads(self.options)
        except (TypeError, json.JSONDecodeError):
            return []

    def set_options(self, options):
        self.options = json.dumps(options)

    options_data = property(get_options, set_options)

    class Meta:
        db_table = 'cars_ml_listing'
        verbose_name = 'Original Car Listing'
        verbose_name_plural = 'Original Car Listings'
        managed = False
        # ordering = ['id']


class CleanedCarListing(models.Model):
    """
    Representation of a cleaned and processed car listing.
    """
    car_listing = models.OneToOneField(CarListing, on_delete=models.CASCADE, primary_key=True)

    listing_url = models.CharField(max_length=255)
    _avg_market_price = models.CharField(max_length=255)

    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    body_type = models.CharField(max_length=255)
    carfax_no_accidents = models.IntegerField()
    carfax_one_owner = models.IntegerField()
    doors = models.IntegerField()
    drivetrain = models.CharField(max_length=255)
    engine_volume = models.FloatField()
    fuel_city = models.FloatField()
    fuel_combined = models.FloatField()
    fuel_highway = models.FloatField()
    fuel_type = models.CharField(max_length=255)
    cylinder = models.IntegerField()
    cylinder_grouped = models.CharField(max_length=255)
    price = models.IntegerField()
    is_new = models.IntegerField()
    is_private = models.IntegerField()
    kms = models.IntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    num_photos = models.IntegerField()
    transmission = models.CharField(max_length=255)
    year = models.IntegerField()

    description_len = models.IntegerField()
    description_premium = models.IntegerField()
    description_luxury = models.IntegerField()
    description_rebuild = models.IntegerField()
    description_sport = models.IntegerField()

    options_qty = models.IntegerField()

    opt_heated_steering_wheel = models.IntegerField(default=0)
    opt_auto_on_off_headlamps = models.IntegerField(default=0)
    opt_illuminated_visor_mirror = models.IntegerField(default=0)
    opt_dual_climate_controls = models.IntegerField(default=0)
    opt_satellite_radio = models.IntegerField(default=0)
    opt_power_brakes = models.IntegerField(default=0)
    opt_anti_theft = models.IntegerField(default=0)
    opt_driver_side_airbag = models.IntegerField(default=0)
    opt_all_wheel_drive = models.IntegerField(default=0)
    opt_memory_seats = models.IntegerField(default=0)
    opt_daytime_running_lights = models.IntegerField(default=0)
    opt_cd_player = models.IntegerField(default=0)
    opt_power_locks = models.IntegerField(default=0)
    opt_auxiliary_12v_outlet = models.IntegerField(default=0)
    opt_remote_starter = models.IntegerField(default=0)
    opt_heated_seats = models.IntegerField(default=0)
    opt_rear_defroster = models.IntegerField(default=0)
    opt_intermittent_wipers = models.IntegerField(default=0)
    opt_power_windows = models.IntegerField(default=0)
    opt_privacy_glass = models.IntegerField(default=0)
    opt_power_seat = models.IntegerField(default=0)
    opt_roll_bar = models.IntegerField(default=0)
    opt_steering_wheel_audio_controls = models.IntegerField(default=0)
    opt_child_safety_locks = models.IntegerField(default=0)
    opt_cruise_control = models.IntegerField(default=0)
    opt_sunroof = models.IntegerField(default=0)
    opt_telescoping_steering = models.IntegerField(default=0)
    opt_power_lift_gates = models.IntegerField(default=0)
    opt_bluetooth = models.IntegerField(default=0)
    opt_cup_holder = models.IntegerField(default=0)
    opt_alloy_wheels = models.IntegerField(default=0)
    opt_anti_lock_brakes_abs = models.IntegerField(default=0)
    opt_leather_wrap_wheel = models.IntegerField(default=0)
    opt_trip_odometer = models.IntegerField(default=0)
    opt_reverse_parking_sensors = models.IntegerField(default=0)
    opt_air_conditioning = models.IntegerField(default=0)
    opt_engine_8cyl = models.IntegerField(default=0)
    opt_fog_lights = models.IntegerField(default=0)
    opt_auto_dimming_mirrors = models.IntegerField(default=0)
    opt_crew_cab = models.IntegerField(default=0)
    opt_split_folding_rear_seats = models.IntegerField(default=0)
    opt_security_system = models.IntegerField(default=0)
    opt_fully_loaded = models.IntegerField(default=0)
    opt_front_wheel_drive = models.IntegerField(default=0)
    opt_6_speed = models.IntegerField(default=0)
    opt_remote_trunk_release = models.IntegerField(default=0)
    opt_rear_window_wiper = models.IntegerField(default=0)
    opt_lane_departure_warning = models.IntegerField(default=0)
    opt_stability_control = models.IntegerField(default=0)
    opt_spoiler = models.IntegerField(default=0)
    opt_power_steering = models.IntegerField(default=0)
    opt_side_impact_airbag = models.IntegerField(default=0)
    opt_am_fm_stereo = models.IntegerField(default=0)
    opt_mp3_cd_player = models.IntegerField(default=0)
    opt_adaptive_cruise_control = models.IntegerField(default=0)
    opt_traction_control = models.IntegerField(default=0)
    opt_digital_clock = models.IntegerField(default=0)
    opt_premium_audio = models.IntegerField(default=0)
    opt_tinted_windows = models.IntegerField(default=0)
    opt_3rd_row_seating = models.IntegerField(default=0)
    opt_remote_start = models.IntegerField(default=0)
    opt_heated_mirrors = models.IntegerField(default=0)
    opt_wood_trim_interior = models.IntegerField(default=0)
    opt_anti_starter = models.IntegerField(default=0)
    opt_power_adjustable_seat = models.IntegerField(default=0)
    opt_xenon_headlights = models.IntegerField(default=0)
    opt_panoramic_sunroof = models.IntegerField(default=0)
    opt_leather_interior = models.IntegerField(default=0)
    opt_navigation_system = models.IntegerField(default=0)
    opt_tilt_steering = models.IntegerField(default=0)
    opt_tachometer = models.IntegerField(default=0)
    opt_tow_package = models.IntegerField(default=0)
    opt_rear_view_camera = models.IntegerField(default=0)
    opt_rear_air_heat = models.IntegerField(default=0)
    opt_power_mirrors = models.IntegerField(default=0)
    opt_rain_sensor_wipers = models.IntegerField(default=0)
    opt_keyless_entry = models.IntegerField(default=0)
    opt_bucket_seats = models.IntegerField(default=0)
    opt_console = models.IntegerField(default=0)
    opt_map_lights = models.IntegerField(default=0)
    opt_climate_control = models.IntegerField(default=0)
    opt_dual_airbag = models.IntegerField(default=0)
    opt_trip_computer = models.IntegerField(default=0)
    opt_cloth_interior = models.IntegerField(default=0)
    opt_passenger_airbag = models.IntegerField(default=0)

    class Meta:
        db_table = 'cleaned_cars_ml_listing'
        verbose_name = 'Cleaned Car Listing'
        verbose_name_plural = 'Cleaned Car Listings'
        managed = False
        # ordering = ['id']


class CarMaker(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'car_makers'
        verbose_name_plural = 'makers'
        managed = False


class CarModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    maker = models.ForeignKey(CarMaker, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'car_models'
        verbose_name_plural = 'models'
        managed = False


class Province(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'provinces'
        verbose_name_plural = 'provinces'
        managed = False


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name_plural = 'cities'
        managed = False


class MachineLearningModel(models.Model):
    name = models.CharField(max_length=100)
    model_file = models.FileField(upload_to='machine_learning_models/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
