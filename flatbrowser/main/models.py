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
  results = models.ManyToManyField(Flat)

# class WishList(models.Model):
#     user = models.ForeignKey(User, related_name='shoplist', on_delete=models.CASCADE)
#     list_name = models.CharField(max_length=20)
#     items = models.ManyToManyField(Product)
#     slug = models.SlugField(max_length=150, db_index=True)

#     def __str__(self):
#         return self.list_name

#     def get_absolute_url(self):
#         return reverse('shop:item_list', args=[self.slug])