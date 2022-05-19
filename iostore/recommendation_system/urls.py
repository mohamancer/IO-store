from django.urls import path
from . import views

from .update_score_matrix import score_matrix_handler_thread

score_matrix_handler_thread()
#print(get_highest_rated_offers(tplist))


urlpatterns = [

]