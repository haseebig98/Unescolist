from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinLengthValidator
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class State(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class Iso(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    description = models.TextField(null=True)
    justification = models.TextField(null=True)
    area_hectares = models.FloatField(null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    region = models.ForeignKey("Region", on_delete=models.CASCADE, null=True)
    iso = models.ForeignKey("Iso", on_delete=models.CASCADE, null=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE, null=True)

    tags = TaggableManager()

    #Comments
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='sites_comments_owned')

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_sites')

    def __str__(self) :
        return self.name




class Fav(models.Model) :
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('site', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.site.name[:10])


class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'