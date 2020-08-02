from django.contrib import admin

from . import models


class PersonAdmin(admin.ModelAdmin):
    fields = ("name",)


class WorldSaveAdmin(admin.ModelAdmin):
    fields = ("how", "who", "when")


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.WorldSave, WorldSaveAdmin)
