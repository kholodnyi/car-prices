from django.urls import path

from .views import CarListingAPIView, CarMakerAPIView, ProvinceAPIView, URLPredictionAPIView

urlpatterns = [
    path('predict-by-url/', URLPredictionAPIView.as_view(), name='predict_by_url'),
    path('predict-price/', CarListingAPIView.as_view(), name='predict_price'),
    path('car-makers/<int:id>/', CarMakerAPIView.as_view(), name='car-makers'),
    path('provinces/<int:id>/', ProvinceAPIView.as_view(), name='provinces'),
]
