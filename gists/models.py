from django.db import models


class Owner(models.Model):
    login = models.TextField()
    gists_url = models.TextField()


class GistFile(models.Model):
    filename = models.TextField()
    type = models.TextField()
    language = models.TextField()
    raw_url = models.TextField()
    size = models.IntegerField()


class Gist(models.Model):
    url = models.TextField()
    forks_url = models.TextField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    files = models.ForeignKey(GistFile, on_delete=models.CASCADE)
