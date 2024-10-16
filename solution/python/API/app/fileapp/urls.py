from django.urls import path

from .views import FileStatView, FileReadView


app_name = 'fileapp'

urlpatterns = [
    path('<uuid:uuid>/stat/', FileStatView.as_view(), name='file-stat'),
    path('<uuid:uuid>/read/', FileReadView.as_view(), name='file-read'),
]