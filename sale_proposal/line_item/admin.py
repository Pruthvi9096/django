from django.contrib import admin
from .models import (
    Opportunity,
    Template,LineItem,
    OpportunityTemplates,
    TemplateLineItems,
    LineItemType,
    ChargeCategory,
    Contact,
    SaleProposal,
    OrderLine
)

admin.site.register(Opportunity)
admin.site.register(Template)
admin.site.register(LineItem)
admin.site.register(OpportunityTemplates)
admin.site.register(TemplateLineItems)
admin.site.register(LineItemType)
admin.site.register(ChargeCategory)
admin.site.register(Contact)
admin.site.register(SaleProposal)
admin.site.register(OrderLine)