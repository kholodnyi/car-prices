from django.views.generic import ListView
from django.shortcuts import render
from django.views import View

from .forms import CarListingForm, URLForm
from .models import CarListing, CarMaker, Province


class RandomCarsView(ListView):
    model = CarListing
    template_name = 'random_cars.html'
    context_object_name = 'cars'
    queryset = CarListing.objects.order_by('?')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Random Cars'
        return context


class CarListingPredictionView(View):
    template_name = 'car_listing_form.html'

    def get(self, request):
        car_makers = CarMaker.objects.all()
        provinces = Province.objects.all()
        form = CarListingForm()
        context = {
            'form': form,
            'car_makers': car_makers,
            'provinces': provinces,
        }

        return render(request, self.template_name, context)


class ByURLPredictionView(View):
    template_name = 'url_form.html'

    def get(self, request):
        form = URLForm()
        context = {
            'form': form,
        }

        return render(request, self.template_name, context)
