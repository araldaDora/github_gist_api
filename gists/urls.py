from django.urls import path
from .views import (
    homepage,
    display_gist_file_content
)

urlpatterns = [
    path("", homepage, name="gist-app-home"),
    path("read-gist-file/", display_gist_file_content, name="display-gist-file-content")
]
