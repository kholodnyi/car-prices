# Generated by Django 4.2.1 on 2023-05-13 05:37

import cars.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_id', models.IntegerField(unique=True)),
                ('listing_url', models.CharField(max_length=255)),
                ('_avg_market_price', models.CharField(max_length=255)),
                ('body_type', models.CharField(max_length=255)),
                ('carfax_no_accidents', models.IntegerField()),
                ('carfax_one_owner', models.IntegerField()),
                ('cylinder', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('doors', models.IntegerField()),
                ('drivetrain', models.CharField(max_length=255)),
                ('engine', models.CharField(max_length=255)),
                ('fuel_city', models.FloatField()),
                ('fuel_combined', models.FloatField()),
                ('fuel_highway', models.FloatField()),
                ('fuel_type', models.CharField(max_length=255)),
                ('is_new', models.IntegerField()),
                ('is_private', models.IntegerField()),
                ('kms', models.IntegerField()),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('num_photos', models.IntegerField()),
                ('options', cars.models.RawJSONField()),
                ('price', models.IntegerField()),
                ('status', models.CharField(max_length=255)),
                ('transmission', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('bad_data', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Original Car Listing',
                'verbose_name_plural': 'Original Car Listings',
                'db_table': 'cars_ml_listing',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CarMaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'makers',
                'db_table': 'car_makers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'models',
                'db_table': 'car_models',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'cities',
                'db_table': 'cities',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'provinces',
                'db_table': 'provinces',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MachineLearningModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model_file', models.FileField(upload_to='machine_learning_models/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CleanedCarListing',
            fields=[
                ('car_listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='cars.carlisting')),
                ('listing_url', models.CharField(max_length=255)),
                ('_avg_market_price', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('body_type', models.CharField(max_length=255)),
                ('carfax_no_accidents', models.IntegerField()),
                ('carfax_one_owner', models.IntegerField()),
                ('doors', models.IntegerField()),
                ('drivetrain', models.CharField(max_length=255)),
                ('engine_volume', models.FloatField()),
                ('fuel_city', models.FloatField()),
                ('fuel_combined', models.FloatField()),
                ('fuel_highway', models.FloatField()),
                ('fuel_type', models.CharField(max_length=255)),
                ('cylinder', models.IntegerField()),
                ('cylinder_grouped', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('is_new', models.IntegerField()),
                ('is_private', models.IntegerField()),
                ('kms', models.IntegerField()),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('num_photos', models.IntegerField()),
                ('transmission', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('description_len', models.IntegerField()),
                ('description_premium', models.IntegerField()),
                ('description_luxury', models.IntegerField()),
                ('description_rebuild', models.IntegerField()),
                ('description_sport', models.IntegerField()),
                ('options_qty', models.IntegerField()),
                ('opt_heated_steering_wheel', models.IntegerField(default=0)),
                ('opt_auto_on_off_headlamps', models.IntegerField(default=0)),
                ('opt_illuminated_visor_mirror', models.IntegerField(default=0)),
                ('opt_dual_climate_controls', models.IntegerField(default=0)),
                ('opt_satellite_radio', models.IntegerField(default=0)),
                ('opt_power_brakes', models.IntegerField(default=0)),
                ('opt_anti_theft', models.IntegerField(default=0)),
                ('opt_driver_side_airbag', models.IntegerField(default=0)),
                ('opt_all_wheel_drive', models.IntegerField(default=0)),
                ('opt_memory_seats', models.IntegerField(default=0)),
                ('opt_daytime_running_lights', models.IntegerField(default=0)),
                ('opt_cd_player', models.IntegerField(default=0)),
                ('opt_power_locks', models.IntegerField(default=0)),
                ('opt_auxiliary_12v_outlet', models.IntegerField(default=0)),
                ('opt_remote_starter', models.IntegerField(default=0)),
                ('opt_heated_seats', models.IntegerField(default=0)),
                ('opt_rear_defroster', models.IntegerField(default=0)),
                ('opt_intermittent_wipers', models.IntegerField(default=0)),
                ('opt_power_windows', models.IntegerField(default=0)),
                ('opt_privacy_glass', models.IntegerField(default=0)),
                ('opt_power_seat', models.IntegerField(default=0)),
                ('opt_roll_bar', models.IntegerField(default=0)),
                ('opt_steering_wheel_audio_controls', models.IntegerField(default=0)),
                ('opt_child_safety_locks', models.IntegerField(default=0)),
                ('opt_cruise_control', models.IntegerField(default=0)),
                ('opt_sunroof', models.IntegerField(default=0)),
                ('opt_telescoping_steering', models.IntegerField(default=0)),
                ('opt_power_lift_gates', models.IntegerField(default=0)),
                ('opt_bluetooth', models.IntegerField(default=0)),
                ('opt_cup_holder', models.IntegerField(default=0)),
                ('opt_alloy_wheels', models.IntegerField(default=0)),
                ('opt_anti_lock_brakes_abs', models.IntegerField(default=0)),
                ('opt_leather_wrap_wheel', models.IntegerField(default=0)),
                ('opt_trip_odometer', models.IntegerField(default=0)),
                ('opt_reverse_parking_sensors', models.IntegerField(default=0)),
                ('opt_air_conditioning', models.IntegerField(default=0)),
                ('opt_engine_8cyl', models.IntegerField(default=0)),
                ('opt_fog_lights', models.IntegerField(default=0)),
                ('opt_auto_dimming_mirrors', models.IntegerField(default=0)),
                ('opt_crew_cab', models.IntegerField(default=0)),
                ('opt_split_folding_rear_seats', models.IntegerField(default=0)),
                ('opt_security_system', models.IntegerField(default=0)),
                ('opt_fully_loaded', models.IntegerField(default=0)),
                ('opt_front_wheel_drive', models.IntegerField(default=0)),
                ('opt_6_speed', models.IntegerField(default=0)),
                ('opt_remote_trunk_release', models.IntegerField(default=0)),
                ('opt_rear_window_wiper', models.IntegerField(default=0)),
                ('opt_lane_departure_warning', models.IntegerField(default=0)),
                ('opt_stability_control', models.IntegerField(default=0)),
                ('opt_spoiler', models.IntegerField(default=0)),
                ('opt_power_steering', models.IntegerField(default=0)),
                ('opt_side_impact_airbag', models.IntegerField(default=0)),
                ('opt_am_fm_stereo', models.IntegerField(default=0)),
                ('opt_mp3_cd_player', models.IntegerField(default=0)),
                ('opt_adaptive_cruise_control', models.IntegerField(default=0)),
                ('opt_traction_control', models.IntegerField(default=0)),
                ('opt_digital_clock', models.IntegerField(default=0)),
                ('opt_premium_audio', models.IntegerField(default=0)),
                ('opt_tinted_windows', models.IntegerField(default=0)),
                ('opt_3rd_row_seating', models.IntegerField(default=0)),
                ('opt_remote_start', models.IntegerField(default=0)),
                ('opt_heated_mirrors', models.IntegerField(default=0)),
                ('opt_wood_trim_interior', models.IntegerField(default=0)),
                ('opt_anti_starter', models.IntegerField(default=0)),
                ('opt_power_adjustable_seat', models.IntegerField(default=0)),
                ('opt_xenon_headlights', models.IntegerField(default=0)),
                ('opt_panoramic_sunroof', models.IntegerField(default=0)),
                ('opt_leather_interior', models.IntegerField(default=0)),
                ('opt_navigation_system', models.IntegerField(default=0)),
                ('opt_tilt_steering', models.IntegerField(default=0)),
                ('opt_tachometer', models.IntegerField(default=0)),
                ('opt_tow_package', models.IntegerField(default=0)),
                ('opt_rear_view_camera', models.IntegerField(default=0)),
                ('opt_rear_air_heat', models.IntegerField(default=0)),
                ('opt_power_mirrors', models.IntegerField(default=0)),
                ('opt_rain_sensor_wipers', models.IntegerField(default=0)),
                ('opt_keyless_entry', models.IntegerField(default=0)),
                ('opt_bucket_seats', models.IntegerField(default=0)),
                ('opt_console', models.IntegerField(default=0)),
                ('opt_map_lights', models.IntegerField(default=0)),
                ('opt_climate_control', models.IntegerField(default=0)),
                ('opt_dual_airbag', models.IntegerField(default=0)),
                ('opt_trip_computer', models.IntegerField(default=0)),
                ('opt_cloth_interior', models.IntegerField(default=0)),
                ('opt_passenger_airbag', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Cleaned Car Listing',
                'verbose_name_plural': 'Cleaned Car Listings',
                'db_table': 'cleaned_cars_ml_listing',
                'managed': False,
            },
        ),
    ]
