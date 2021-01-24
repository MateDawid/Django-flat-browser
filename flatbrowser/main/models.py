from django.db import models

class Flat(models.Model):
  site = models.CharField(max_length=200)
  city = models.CharField(max_length=200)
  title = models.CharField(max_length=200)
  area = models.IntegerField()
  price = models.IntegerField()
  url = models.URLField()
  image = models.URLField()

  def __str__(self):
      return (f"{self.id} | {self.site} | {self.city} | {self.title}")

class SearchingResult(models.Model):
  date = models.DateTimeField(auto_now_add=True)
  results = models.ManyToManyField(Flat)
