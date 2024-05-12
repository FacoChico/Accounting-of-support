from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Категория {self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Logistics(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    quantity_available = models.IntegerField(default=0)

    def __str__(self):
        return f'"{self.name}" из категории "{self.category.name}" типа "{self.type}"'

    class Meta:
        verbose_name = "Logistics"
        verbose_name_plural = "Logistics"
