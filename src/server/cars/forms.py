from django import forms


class CarListingForm(forms.Form):
    drivetrain_choices = [('4WD', '4WD'), ('2WD', '2WD'), ]
    fuel_choices = [('Flexible', 'Flexible'), ('Diesel', 'Diesel'), ('Gasoline', 'Gasoline'), ('Hybrid', 'Hybrid'), ]
    transmission_choices = [('Automatic', 'Automatic'), ('Manual', 'Manual'), ]
    body_type_choices = [
        ('Station Wagon', 'Station Wagon'),
        ('Crew Cab', 'Crew Cab'),
        ('Hatchback', 'Hatchback'),
        ('Super Crew', 'Super Crew'),
        ('SUV', 'SUV'),
        ('Truck Long Regular Cab', 'Truck Long Regular Cab'),
        ('Truck Crew Cab', 'Truck Crew Cab'),
        ('Mega Cab', 'Mega Cab'),
        ('Roadster', 'Roadster'),
        ('Truck Quad Cab', 'Truck Quad Cab'),
        ('Convertible', 'Convertible'),
        ('Truck Super Cab', 'Truck Super Cab'),
        ('Regular Cab', 'Regular Cab'),
        ('Extended Cab', 'Extended Cab'),
        ('Super Cab', 'Super Cab'),
        ('Sedan', 'Sedan'),
        ('Wagon', 'Wagon'),
        ('Van Extended', 'Van Extended'),
        ('Truck Long Extended Cab', 'Truck Long Extended Cab'),
        ('Truck Short Mega Cab', 'Truck Short Mega Cab'),
        ('Truck Short Quad Cab', 'Truck Short Quad Cab'),
        ('Truck Long Double Cab', 'Truck Long Double Cab'),
        ('Truck Chassis', 'Truck Chassis'),
        ('Van Regular', 'Van Regular'),
        ('Compact', 'Compact'),
        ('Truck Short Double Cab', 'Truck Short Double Cab'),
        ('Truck Double Cab', 'Truck Double Cab'),
        ('Truck Extended Cab', 'Truck Extended Cab'),
        ('Cabriolet', 'Cabriolet'),
        ('Truck Short Crew Cab', 'Truck Short Crew Cab'),
        ('Coupe', 'Coupe'),
        ('Truck Regular Cab', 'Truck Regular Cab'),
        ('Truck Long Crew Cab', 'Truck Long Crew Cab'),
        ('Cutaway', 'Cutaway'),
        ('Quad Cab', 'Quad Cab'),
        ('Minivan', 'Minivan'),
        ('Truck', 'Truck'),
    ]

    carfax_no_accidents = forms.BooleanField(required=False)
    carfax_one_owner = forms.BooleanField(required=False)
    doors = forms.IntegerField()
    body_type = forms.ChoiceField(choices=body_type_choices)
    drivetrain = forms.ChoiceField(choices=drivetrain_choices)
    fuel_type = forms.ChoiceField(choices=fuel_choices)
    transmission = forms.ChoiceField(choices=transmission_choices)
    cylinder = forms.IntegerField()
    is_new = forms.BooleanField(required=False)
    is_private = forms.BooleanField(required=False)
    kms = forms.IntegerField()
    num_photos = forms.IntegerField()
    year = forms.IntegerField()
    description_len = forms.IntegerField(required=False)
    description_premium = forms.BooleanField(required=False)
    description_luxury = forms.BooleanField(required=False)
    description_rebuild = forms.BooleanField(required=False)
    description_sport = forms.BooleanField(required=False)

    opt_heated_steering_wheel = forms.BooleanField(required=False)
    opt_auto_on_off_headlamps = forms.BooleanField(required=False)
    opt_illuminated_visor_mirror = forms.BooleanField(required=False)
    opt_dual_climate_controls = forms.BooleanField(required=False)
    opt_satellite_radio = forms.BooleanField(required=False)
    opt_power_brakes = forms.BooleanField(required=False)
    opt_anti_theft = forms.BooleanField(required=False)
    opt_driver_side_airbag = forms.BooleanField(required=False)
    opt_all_wheel_drive = forms.BooleanField(required=False)
    opt_memory_seats = forms.BooleanField(required=False)
    opt_daytime_running_lights = forms.BooleanField(required=False)
    opt_cd_player = forms.BooleanField(required=False)
    opt_power_locks = forms.BooleanField(required=False)
    opt_auxiliary_12v_outlet = forms.BooleanField(required=False)
    opt_remote_starter = forms.BooleanField(required=False)
    opt_heated_seats = forms.BooleanField(required=False)
    opt_rear_defroster = forms.BooleanField(required=False)
    opt_intermittent_wipers = forms.BooleanField(required=False)
    opt_power_windows = forms.BooleanField(required=False)
    opt_privacy_glass = forms.BooleanField(required=False)
    opt_power_seat = forms.BooleanField(required=False)
    opt_roll_bar = forms.BooleanField(required=False)
    opt_steering_wheel_audio_controls = forms.BooleanField(required=False)
    opt_child_safety_locks = forms.BooleanField(required=False)
    opt_cruise_control = forms.BooleanField(required=False)
    opt_sunroof = forms.BooleanField(required=False)
    opt_telescoping_steering = forms.BooleanField(required=False)
    opt_power_lift_gates = forms.BooleanField(required=False)
    opt_bluetooth = forms.BooleanField(required=False)
    opt_cup_holder = forms.BooleanField(required=False)
    opt_alloy_wheels = forms.BooleanField(required=False)
    opt_anti_lock_brakes_abs = forms.BooleanField(required=False)
    opt_leather_wrap_wheel = forms.BooleanField(required=False)
    opt_trip_odometer = forms.BooleanField(required=False)
    opt_reverse_parking_sensors = forms.BooleanField(required=False)
    opt_air_conditioning = forms.BooleanField(required=False)
    opt_engine_8cyl = forms.BooleanField(required=False)
    opt_fog_lights = forms.BooleanField(required=False, )
    opt_auto_dimming_mirrors = forms.BooleanField(required=False)
    opt_crew_cab = forms.BooleanField(required=False)
    opt_split_folding_rear_seats = forms.BooleanField(required=False)
    opt_security_system = forms.BooleanField(required=False)
    opt_fully_loaded = forms.BooleanField(required=False)
    opt_front_wheel_drive = forms.BooleanField(required=False)
    opt_6_speed = forms.BooleanField(required=False)
    opt_remote_trunk_release = forms.BooleanField(required=False)
    opt_rear_window_wiper = forms.BooleanField(required=False)
    opt_lane_departure_warning = forms.BooleanField(required=False)
    opt_stability_control = forms.BooleanField(required=False)
    opt_spoiler = forms.BooleanField(required=False)
    opt_power_steering = forms.BooleanField(required=False)
    opt_side_impact_airbag = forms.BooleanField(required=False)
    opt_am_fm_stereo = forms.BooleanField(required=False)
    opt_mp3_cd_player = forms.BooleanField(required=False)
    opt_adaptive_cruise_control = forms.BooleanField(required=False)
    opt_traction_control = forms.BooleanField(required=False)
    opt_digital_clock = forms.BooleanField(required=False)
    opt_premium_audio = forms.BooleanField(required=False)
    opt_tinted_windows = forms.BooleanField(required=False)
    opt_3rd_row_seating = forms.BooleanField(required=False)
    opt_remote_start = forms.BooleanField(required=False)
    opt_heated_mirrors = forms.BooleanField(required=False)
    opt_wood_trim_interior = forms.BooleanField(required=False)
    opt_anti_starter = forms.BooleanField(required=False)
    opt_power_adjustable_seat = forms.BooleanField(required=False)
    opt_xenon_headlights = forms.BooleanField(required=False)
    opt_panoramic_sunroof = forms.BooleanField(required=False)
    opt_leather_interior = forms.BooleanField(required=False)
    opt_navigation_system = forms.BooleanField(required=False)
    opt_tilt_steering = forms.BooleanField(required=False)
    opt_tachometer = forms.BooleanField(required=False)
    opt_tow_package = forms.BooleanField(required=False)
    opt_rear_view_camera = forms.BooleanField(required=False)
    opt_rear_air_heat = forms.BooleanField(required=False)
    opt_power_mirrors = forms.BooleanField(required=False)
    opt_rain_sensor_wipers = forms.BooleanField(required=False)
    opt_keyless_entry = forms.BooleanField(required=False)
    opt_bucket_seats = forms.BooleanField(required=False)
    opt_console = forms.BooleanField(required=False)
    opt_map_lights = forms.BooleanField(required=False)
    opt_climate_control = forms.BooleanField(required=False)
    opt_dual_airbag = forms.BooleanField(required=False)
    opt_trip_computer = forms.BooleanField(required=False)
    opt_cloth_interior = forms.BooleanField(required=False)
    opt_passenger_airbag = forms.BooleanField(required=False)

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1985 or year > 2024:
            raise forms.ValidationError('Invalid year')
        return year

    def clean_kms(self):
        kms = self.cleaned_data['kms']
        if kms >= 500000:
            raise forms.ValidationError('Invalid kms')
        return kms


class URLForm(forms.Form):
    url = forms.URLField()
