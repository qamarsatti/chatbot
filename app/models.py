from django.contrib.auth.models import User
from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)


class PDFEmbedding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    embedding = VectorField(dimensions=1536)
