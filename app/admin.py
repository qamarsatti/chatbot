from django.contrib import admin

from app.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "document_name")
