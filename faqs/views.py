from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer


class FAQListCreateView(generics.ListCreateAPIView):
    """
    View to list all FAQs or create a new FAQ.
    - Supports GET requests to retrieve all FAQ objects.
    - Supports POST requests to create a new FAQ.
    """
    queryset = FAQ.objects.all()  # Get all FAQ objects from the database
    serializer_class = FAQSerializer  # Use the FAQSerializer to format data


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete an FAQ.
    - Supports GET requests to retrieve a specific FAQ by its ID.
    - Supports PUT and PATCH requests to update an FAQ.
    - Supports DELETE requests to remove an FAQ.
    """
    queryset = FAQ.objects.all()  # Get FAQ object by ID from the database
    serializer_class = FAQSerializer  # Use the FAQSerializer to format data

    def get_serializer_context(self):
        """
        Override to pass the request context to the serializer.
        This is useful for the serializer to know about the request.
        """
        return {'request': self.request}
