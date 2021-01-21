from django.db import models

class Flat(models.Model):
  site = models.CharField(max_length=200)
  city = models.CharField(max_length=200)
  title = models.CharField(max_length=200)
  area = models.FloatField(blank=True, null=True)
  price = models.FloatField()
  url = models.URLField()
  image = models.URLField()

  def __str__(self):
      return (f"{self.id} | {self.site} | {self.city} | {self.title}")

