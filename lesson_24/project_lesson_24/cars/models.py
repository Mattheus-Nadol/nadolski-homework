from django.db import models

# Create your models here.
class Dealer(models.Model):
    name = models.CharField()
    address = models.TextField()

    def __str__(self):
        return f"Dealer: {self.name}"

class Car(models.Model):
    brand = models.CharField()
    model = models.CharField()
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(null=True, blank=True)
    owner_website = models.URLField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"
    
