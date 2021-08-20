from django.contrib import admin

from applications.main.models import BuildingObject, ConstructionMaterial


class BuildingObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create')
    list_display_links = ('name', )
    search_fields = ('name', )
    list_filter = ('time_create',)


class ConstructionMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'price', 'total_cost', 'building_object')
    list_display_links = ('name', )
    search_fields = ('name', )


admin.site.register(BuildingObject, BuildingObjectAdmin)
admin.site.register(ConstructionMaterial, ConstructionMaterialAdmin)

