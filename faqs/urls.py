from django.urls import path
from .views import FAQListCreateView, FAQDetailView

urlpatterns = [
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]
