from django.urls import path
from .views import RandomCarsView, CarListingPredictionView, ByURLPredictionView

urlpatterns = [
    path('random-cars/', RandomCarsView.as_view(), name='random_cars'),
    path('car-listing-prediction/', CarListingPredictionView.as_view(), name='car_listing_prediction'),
    path('url-prediction/', ByURLPredictionView.as_view(), name='url_prediction'),
]
