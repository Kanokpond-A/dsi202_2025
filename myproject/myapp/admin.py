from django.contrib import admin
from .models import Tree, PlantingPlan, Equipment, Purchase

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'preferred_area')

@admin.register(PlantingPlan)
class PlantingPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_name', 'trees_per_month', 'start_date', 'end_date')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'tree', 'equipment', 'quantity', 'total_price', 'purchase_date')
