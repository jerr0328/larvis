from django.views.generic import ListView

from .models import WorldSave


class WorldSaveList(ListView):
    model = WorldSave
    ordering = ["-when"]
