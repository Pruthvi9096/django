from django.db import models


class LineItemType(models.Model):

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class ChargeCategory(models.Model):

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class LineItem(models.Model):

    name = models.CharField(max_length=250)
    item_id = models.CharField(max_length=25, verbose_name='Item ID', null=True, blank=True)
    item_detail_id = models.CharField(
        max_length=25, verbose_name='Item Detail ID', null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    discount_allowed = models.BooleanField(default=False)
    max_discount = models.DecimalField(max_digits=7, decimal_places=2)
    line_item_type = models.ForeignKey(LineItemType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Template(models.Model):

    name = models.CharField(max_length=250)
    template_id = models.CharField(max_length=25, verbose_name='Template ID', null=True, blank=True)
    purchase_type = models.CharField(max_length=50,choices=[('perpetual','Perpetual'),('monthly_subscription','Monthly Subscription')],null=True,blank=True)

    def __str__(self):
        return self.name


class Opportunity(models.Model):

    name = models.CharField(max_length=250)
    opportunity_id = models.CharField(
        max_length=25, verbose_name='Opportunity ID', null=True, blank=True)

    def __str__(self):
        return self.name


class OpportunityTemplates(models.Model):

    opportunity = models.ForeignKey(Opportunity,on_delete=models.CASCADE,related_name='templates')
    template = models.ForeignKey(Template,on_delete=models.CASCADE)
    charge_category = models.ForeignKey(ChargeCategory,on_delete=models.SET_NULL,null=True,blank=True)


class TemplateLineItems(models.Model):

    template = models.ForeignKey(Template,on_delete=models.CASCADE, related_name='line_items')
    line_item = models.ForeignKey(LineItem,on_delete=models.CASCADE)
