# admin.py

from django.contrib import admin
from .models import FAQ

# Admin view for FAQ model.


class FAQAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing FAQ objects.
    - 'list_display' specifies the fields to display in the list view.
    - 'search_fields' allows searching FAQs by 'question' and translations.
    """
    # Display the 'question' field in the list view
    list_display = ('question',)
    # Enable searching by 'question' and translations
    search_fields = ('question', 'question_hi', 'question_bn')

# Register the FAQ model with the custom admin view.


admin.site.register(FAQ, FAQAdmin)
