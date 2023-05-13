from django.contrib import admin
from .models import CarListing, CleanedCarListing, CarMaker, CarModel, Province, City, MachineLearningModel


@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('listing_id', 'make', 'model', 'year', 'price', 'status', 'bad_data')
    list_filter = ('bad_data', 'model', 'year', 'status')
    search_fields = ('make', 'model', 'year', 'price')


@admin.register(CleanedCarListing)
class CleanedCarListingAdmin(admin.ModelAdmin):
    list_display = ('car_listing', 'make', 'model', 'year', 'price')
    list_filter = ('year', )
    search_fields = ('make', 'model', 'year', 'price')


@admin.register(CarMaker)
class CarMakerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'maker')
    list_filter = ('maker',)
    search_fields = ('name',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)
    search_fields = ('name',)


@admin.register(MachineLearningModel)
class MachineLearningModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_file']

    def __str__(self):
        return self.name
