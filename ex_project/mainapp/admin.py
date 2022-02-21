from django.contrib import admin
from .models import User, ExcelFile

class ExcelAdmin(admin.ModelAdmin):
    list_display = ('excel_file', 'uploaded_at', 'handled_at', 'handle_status', 'result', 'user')
    list_display_links = ('excel_file','uploaded_at')
admin.site.register(User)
admin.site.register(ExcelFile,ExcelAdmin)
