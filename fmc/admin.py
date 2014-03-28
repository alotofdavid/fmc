from fmc.models import Scramble, Submission
from django.contrib import admin

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 3

class ScrambleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['scramble']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [SubmissionInline]

admin.site.register(Scramble, ScrambleAdmin)