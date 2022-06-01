from django.urls import path
from . import views

from .update_score_matrix import matrices_handler_thread

try: # this will fail if the data base is not initialized yet, should work in any other case, im just putting it here
    #so we will not get an uncatched error in the thread when making migrations
    matrices_handler_thread()
except:
    pass



urlpatterns = [

]