from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

UPFRONT_DEPOSITS = [
    ('25', '25'),
    ('50', '50'),
    ('75', '75'),
    ('100', '100'),
    ('other', 'Other'),
    ('amount', 'Amount')
]


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
    item_id = models.CharField(
        max_length=25, verbose_name='Item ID', null=True, blank=True)
    item_detail_id = models.CharField(
        max_length=25, verbose_name='Item Detail ID', null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    discount_allowed = models.BooleanField(default=False)
    max_discount = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True)
    line_item_type = models.ForeignKey(
        LineItemType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Template(models.Model):

    name = models.CharField(max_length=250)
    template_id = models.CharField(
        max_length=25, verbose_name='Template ID', null=True, blank=True)
    purchase_type = models.CharField(max_length=50, choices=[(
        'perpetual', 'Perpetual'), ('monthly_subscription', 'Monthly Subscription')], null=True, blank=True)

    def __str__(self):
        return self.name


class Opportunity(models.Model):

    name = models.CharField(max_length=250)
    opportunity_id = models.CharField(
        max_length=25, verbose_name='Opportunity ID', null=True, blank=True)

    def __str__(self):
        return self.name


class OpportunityTemplates(models.Model):

    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name='templates')
    template = models.ForeignKey(Template, on_delete=models.CASCADE)


class TemplateLineItems(models.Model):

    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name='line_items')
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    charge_category = models.ForeignKey(
        ChargeCategory, on_delete=models.SET_NULL, null=True, blank=True)


class Contact(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    child_contacts = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class SaleProposal(models.Model):

    name = models.CharField(max_length=150)
    contact_for = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='proposals',null=True)
    attention_to = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True)
    valid_upto = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True)
    discount_method = models.CharField(max_length=50, choices=[(
        'fixed', 'Fixed'), ('percentage', '%')], default='percentage', blank=True)
    monthlies_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    setup_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    upfront_deposit = models.CharField(
        max_length=50, choices=UPFRONT_DEPOSITS, null=True, blank=True)
    upfront_deposit_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    balance_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    balance_distribution = models.BooleanField(null=True, blank=True)
    balance_distribution_type = models.CharField(max_length=50, choices=[(
        'days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], null=True, blank=True)
    amount_at_execution_of_contract = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)


class OrderLine(models.Model):

    proposal = models.ForeignKey(SaleProposal, on_delete=models.CASCADE)
    product = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    charge_category = models.ForeignKey(
        ChargeCategory, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    item_discount = models.BooleanField(null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
