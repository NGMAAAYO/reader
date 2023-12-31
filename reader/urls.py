from django.urls import re_path, path
 
from . import view
 
urlpatterns = [
    re_path('^reader$', view.reader),
    re_path('^$', view.view),
]