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

# Register your models here.
admin.site.register(Record)
admin.site.register(UserGroup, UserGroupAdmin)