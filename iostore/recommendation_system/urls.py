from django.urls import path
from . import views

from .calc_score import get_highest_rated_offers
tplist = [(0,5), (4, 1), (5,1)]

print(get_highest_rated_offers(tplist))


urlpatterns = [

]