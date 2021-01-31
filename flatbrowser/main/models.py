from django.db import models
from django.contrib.auth.models import User

class Flat(models.Model):
  site = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  title = models.CharField(max_length=100)
  area = models.IntegerField()
  price = models.IntegerField()
  url = models.URLField(max_length=1000)
  image = models.URLField(max_length=1000)
  date = models.DateField()

  def __str__(self):
      return (f"{self.id} | {self.site} | {self.city} | {self.title}")

class WatchedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offers = models.ManyToManyField(Flat)

    def __str__(self):
        return f"{self.user}'s WatchedList"
