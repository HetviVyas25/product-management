from django.contrib import admin

# Register your models here.
from core import models as core_models


admin.site.register(core_models.Customer)
admin.site.register(core_models.Address)
admin.site.register(core_models.Category)
admin.site.register(core_models.SubCategory)
admin.site.register(core_models.Product)
admin.site.register(core_models.AddToCart)



admin.site.site_header = "Product Management"
# admin.site.index_title = ""
admin.site.site_title ="Product Management"