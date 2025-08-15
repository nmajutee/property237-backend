from django.contrib import admin
from .models import AgentProfile, AgentCertification, AgentReview, AgentAchievement, AgentSchedule, AgentContact

@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user','agency_name','is_verified','is_featured','total_sales')
    search_fields = ('user__email','agency_name')

admin.site.register(AgentCertification)
admin.site.register(AgentReview)
admin.site.register(AgentAchievement)
admin.site.register(AgentSchedule)
admin.site.register(AgentContact)
