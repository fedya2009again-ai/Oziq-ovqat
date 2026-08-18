from django.contrib import admin
from .models import Recipe, RecipeStep


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'servings', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    inlines = [RecipeStepInline]


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'step_number', 'title', 'time_minutes')
    list_filter = ('recipe',)