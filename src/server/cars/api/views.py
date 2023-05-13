import sys
import os

# Add the path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(PROJECT_ROOT)

from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from data.ml.utils import get_single_listing_df
from data.models import CarListing
from data.processing import CarListingCleaner
from data.scrapper import Scrapper
from ..models import CarMaker, Province
from ..forms import CarListingForm, URLForm
from .serializers import CarMakerSerializer, ProvinceSerializer
from ..utils import transform_from_input, make_prediction


class CarListingAPIView(APIView):
    def post(self, request, format=None):
        form = CarListingForm(request.POST)

        if form.is_valid():
            try:
                # Process the form data and perform prediction
                data = form.cleaned_data

                # also pass in the request.POST data (separate City, Province, Make, Model)
                df = transform_from_input(data, request.POST)

                return Response({'prediction': make_prediction(df)})
            except Exception as e:
                return Response({'error': str(e)})
        else:
            return Response({'error': form.errors})


class URLPredictionAPIView(APIView):
    def post(self, request, format=None):
        form = URLForm(request.POST)

        if form.is_valid():
            try:
                # Process the form data and perform prediction
                listing_data = Scrapper.scrape_one_listing(form.cleaned_data['url'])
                listing = CarListing(**listing_data)

                cleaner = CarListingCleaner(None)
                cleaned_listing = cleaner._clean_car_listing(listing)

                df = get_single_listing_df(cleaned_listing)

                return Response({'prediction': make_prediction(df)})
            except Exception as e:
                return Response({'error': {'Bad listing': [str(e), ]}, })
        else:
            return Response({'error': form.errors})


class CarMakerAPIView(RetrieveAPIView):
    queryset = CarMaker.objects.prefetch_related('carmodel_set')
    serializer_class = CarMakerSerializer
    lookup_field = 'id'


class ProvinceAPIView(RetrieveAPIView):
    queryset = Province.objects.prefetch_related('city_set')
    serializer_class = ProvinceSerializer
    lookup_field = 'id'
