from typing import Any
from django.contrib import admin
from .models import Record, UserGroup
from .forms import AddGroupForm


class UserGroupAdmin(admin.ModelAdmin):
    form = AddGroupForm

    
    def save_model(self, request, obj, form, change):
        # This is a new object being added
        if not change:  
            obj.admin = request.user
        super().save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change) -> None:
        super().save_related(request, form, formsets, change)
        form.instance.members.add(request.user)

# Register your models here.
admin.site.register(Record)
admin.site.register(UserGroup, UserGroupAdmin)