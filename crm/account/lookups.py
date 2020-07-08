from ajax_select import register, LookupChannel
from .models import Tag
from django.utils.html import escape

@register('tags')
class TagsLookup(LookupChannel):

    model = Tag

    def get_query(self, q, request):
        return self.model.objects.filter(name=q)
    

    def format_match(self, Tag):
        print("============")
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(Tag)

    def format_item_display(self, Tag):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<span class='badge badge-pill badge-info'>%s</span>" % (escape(Tag.moboList))