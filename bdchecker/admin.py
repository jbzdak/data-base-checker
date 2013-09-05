from bdchecker.models import BDCheckerGradePart, BDCheckerActivity
from django.contrib import admin

# Register your models here.

class BDCheckerPartAdmin(admin.TabularInline):
    model = BDCheckerGradePart
    fields = ['name', 'verifier_name', 'weight', 'required', 'part_type']

class BDCheckerActivityAdmin(admin.ModelAdmin):
    inlines = [
        BDCheckerPartAdmin
    ]

admin.site.register(BDCheckerActivity, BDCheckerActivityAdmin)