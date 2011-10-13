from model2.models import Model2
from django.contrib import admin

class Model2Admin(admin.ModelAdmin):
    fieldsets = (
        (None, 
		{'fields': ('title', 'fieldmodel2', 'pub_date')}
	),
    )

admin.site.register(Model2, Model2Admin)

