from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mylistings")
    curbid = models.ForeignKey('Bid', on_delete=models.DO_NOTHING, null=True, blank=True)
    curprice = models.DecimalField(
        decimal_places=2,
        validators=[MinValueValidator(1)],
        max_digits=10,
    )
    active = models.BooleanField(default=True)
    createdatettime = models.DateTimeField(auto_now_add=True)
    closedatettime = models.DateTimeField(null=True, blank=True)
    startbid = models.DecimalField(
        decimal_places=2,
        validators=[MinValueValidator(1)],
        max_digits=10,
    )
    image = models.URLField(null=True, blank=True)
    category = models.ForeignKey('Category',
        on_delete=models.CASCADE, 
        related_name="catlistings",
        null=True, blank=True)
    watchedby = models.ManyToManyField(User, related_name="mywatchings", blank=True)    

    def __str__(self):
        return f"{self.name} by {self.owner.username}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mycomments")
    datetime = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listcomments")

    def __str__(self):
        return f"{self.text}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mybids")
    bidlisting = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listbids")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    datettime = models.DateTimeField(auto_now_add=True)
    bitten = models.BooleanField(default=False)

    def __str__(self):
        return f"${self.amount} for {self.bidlisting.name} by {self.bidder.username}"

