from django.db import models

# Create your models here.


class Author(models.Model):
    fullname = models.CharField(max_length=30, null=False, unique=True)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=50)
    description = models.CharField(max_length=1500)

    def __str__(self):
        return f"Author: {self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return f"Tag: {self.name}"


class Quote(models.Model):
    quote = models.CharField(max_length=300, null=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Quote: {self.quote}"
