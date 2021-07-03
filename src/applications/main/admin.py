from django.contrib import admin

from applications.main.models import BuildingObject, ConstructionMaterial


class BuildingObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create')
    list_display_links = ('name', )
    search_fields = ('name', )
    # list_editable = ('is_published',)
    list_filter = ('time_create',)


class ConstructionMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'quantity', 'price', 'total_cost', 'building_object')
    list_display_links = ('title', 'name', )
    search_fields = ('title', 'name', )
    # list_editable = ('is_published',)
    # list_filter = ('time_create',)


admin.site.register(BuildingObject, BuildingObjectAdmin)
admin.site.register(ConstructionMaterial, ConstructionMaterialAdmin)

