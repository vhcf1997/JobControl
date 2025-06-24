
from django.contrib import admin
from .models import Project, Job # Importe ambos os modelos

admin.site.register(Project)
admin.site.register(Job)