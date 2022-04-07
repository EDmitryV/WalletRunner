from django.contrib import admin

# Register your models here.
from .models import Area_Store, Areas, Stores, Networks


admin.site.register(Area_Store)
admin.site.register(Areas)
admin.site.register(Stores)
admin.site.register(Networks)