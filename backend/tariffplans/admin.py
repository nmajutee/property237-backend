from django.contrib import admin
from .models import TariffCategory, TariffPlan, PlanFeature, PlanFeatureValue, UserSubscription, SubscriptionUsage, PlanUpgrade

admin.site.register(TariffCategory)
admin.site.register(TariffPlan)
admin.site.register(PlanFeature)
admin.site.register(PlanFeatureValue)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionUsage)
admin.site.register(PlanUpgrade)
