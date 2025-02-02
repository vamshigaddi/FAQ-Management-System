import pytest
from rest_framework import status
from django.urls import reverse
from faqs.models import FAQ
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestFAQAPI:
    client = APIClient()

    def test_get_faqs_no_lang(self):
        """
        Test that FAQs are returned in English when no 'lang' parameter is provided.
        - Creates an FAQ with a question and translation fields.
        - Makes a GET request without the 'lang' parameter.
        - Asserts the response status is OK and the question is in English.
        """
        # Create a FAQ instance
        faq = FAQ.objects.create(
            question="What is your name?",
            answer="<p>My name is ChatGPT.</p>",
            question_hi="क्या आपका नाम है?",
            question_bn="আপনার নাম কী?"
        )

        # Make GET request without lang parameter (default will be English)
        url = reverse('faq-list-create')  # Use the URL name for the FAQ list API
        response = self.client.get(url)

        # Validate the response
        assert response.status_code == status.HTTP_200_OK  # Check if status is OK
        assert response.data[0]['question'] == faq.question  # Ensure question is in English

    def test_get_faqs_with_lang_hi(self):
        """
        Test that FAQs are returned with Hindi translation when 'lang=hi' is specified.
        - Creates an FAQ with a question and translation fields.
        - Makes a GET request with 'lang=hi'.
        - Asserts the response contains the Hindi translation.
        """
        # Create a FAQ instance
        faq = FAQ.objects.create(
            question="Where is the capital of India?",
            answer="<p>New Delhi.</p>",
            question_hi="भारत की राजधानी कहाँ है?",
            question_bn="ভারতের রাজধানী কোথায়?"
        )

        # Make GET request with lang=hi
        url = reverse('faq-list-create') + "?lang=hi"
        response = self.client.get(url)

        # Validate the response
        assert response.status_code == status.HTTP_200_OK  # Ensure the response is OK
        assert response.data[0]['translated_question'] == faq.question_hi  # Check Hindi translation

    def test_get_faqs_with_lang_bn(self):
        """
        Test that FAQs are returned with Bengali translation when 'lang=bn' is specified.
        - Creates an FAQ with a question and translation fields.
        - Makes a GET request with 'lang=bn'.
        - Asserts the response contains the Bengali translation.
        """
        # Create a FAQ instance
        faq = FAQ.objects.create(
            question="What is the capital of India?",
            answer="<p>New Delhi.</p>",
            question_hi="भारत की राजधानी कहाँ है?",
            question_bn="ভারতের রাজধানী কোথায়?"
        )

        # Make GET request with lang=bn
        url = reverse('faq-list-create') + "?lang=bn"
        response = self.client.get(url)

        # Validate the response
        assert response.status_code == status.HTTP_200_OK  # Ensure the response is OK
        assert response.data[0]['translated_question'] == faq.question_bn  # Check Bengali translation

    def test_post_faq(self):
        """
        Test that a new FAQ can be created through the API.
        - Sends a POST request with FAQ data (question and translations).
        - Asserts the response status is '201 Created' and the question is saved.
        """
        # Test creating a FAQ through the API
        data = {
            'question': "What is the capital of India?",
            'answer': "<p>New Delhi.</p>",
            'question_hi': "भारत की राजधानी कहाँ है?",
            'question_bn': "ভারতের রাজধানী কোথায়?"
        }

        url = reverse('faq-list-create')  # Use the URL name for the FAQ list API
        response = self.client.post(url, data, format='json')

        # Validate the response
        assert response.status_code == status.HTTP_201_CREATED  # Ensure the FAQ is created
        # Check that the question is saved correctly
        assert response.data['question'] == data['question']

    def test_translation_fallback(self):
        """
        Test fallback to English if the translation is not available for a given language.
        - Creates a FAQ with missing Bengali translation.
        - Makes a GET request with 'lang=bn' (Bengali translation is missing).
        - Asserts the response falls back to the English question.
        """
        # Create a FAQ instance with missing Bengali translation
        faq = FAQ.objects.create(
            question="What is the capital of India?",
            answer="<p>New Delhi.</p>",
            question_hi="भारत की राजधानी कहाँ है?",
            question_bn=""
        )

        # Make GET request with lang=bn (which is missing translation)
        url = reverse('faq-list-create') + "?lang=bn"
        response = self.client.get(url)

        # Validate the response
        assert response.status_code == status.HTTP_200_OK
        # Fallback to English if translation is missing
        assert response.data[0]['question'] == faq.question
