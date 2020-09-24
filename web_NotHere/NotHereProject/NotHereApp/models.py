from django.db import models

# Create your models here.

class StoreDB(models.Model):
    store_id = models.IntegerField()
    name = models.CharField(max_length=50)
    visitors_reviews = models.IntegerField()
    blog_reviews = models.IntegerField()
    call = models.CharField(max_length=30)
    address = models.TextField()
    operation = models.CharField(max_length=30)
    naver_link = models.TextField()
    score = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    addcode = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id} : {self.name}'

class ReviewDB(models.Model):
    review_id = models.IntegerField()
    store_id = models.ForeignKey(
        StoreDB, related_name='reivew', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, null=True)
    date = models.CharField(max_length=20, null=True)
    score = models.CharField(max_length=10)
    text = models.TextField()

    def __str__(self):
        return f'{self.id} : store_id : {self.store_id}'