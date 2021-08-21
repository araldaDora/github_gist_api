from django.urls import path
from .views import (
    homepage,
    display_gist_file_content,
    display_latest_forks_for_gist
)

urlpatterns = [
    path("", homepage, name="gist-app-home"),
    path("read-gist-file/", display_gist_file_content, name="display-gist-file-content"),
    path("gist-latest-forks/", display_latest_forks_for_gist, name="display-gist-latest-forks")
]
