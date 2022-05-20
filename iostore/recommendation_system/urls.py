from django.urls import path
from . import views

from .update_score_matrix import matrices_handler_thread


matrices_handler_thread()

#print(get_highest_rated_offers(tplist))


urlpatterns = [

]