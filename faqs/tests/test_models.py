import pytest
from faqs.models import FAQ
from django.core.cache import cache


@pytest.mark.django_db
def test_faq_creation():
    """
    Test that a new FAQ can be created with a question and an answer.
    - Creates a new FAQ object.
    - Asserts that the question and answer are correctly stored in the DB.
    """
    faq = FAQ.objects.create(question="What is India?", answer="<p>Country</p>")

    # Check if the question and answer are saved correctly
    assert faq.question == "What is India?"
    assert faq.answer == "<p>Country</p>"


@pytest.mark.django_db
def test_faq_translation():
    """
    Test that the FAQ translations are generated for Hindi and Bengali.
    - Creates a new FAQ object.
    - Asserts that both Hindi and Bengali translations are generated.
    """
    faq = FAQ.objects.create(question="Where is Sriharikota?", answer="<p>AP</p>")

    # Check if translations for Hindi and Bengali are generated
    assert faq.question_hi is not None  # Ensure Hindi translation exists
    assert faq.question_bn is not None  # Ensure Bengali translation exists


@pytest.mark.django_db
def test_faq_caching():
    """
    Test that the FAQ translation is cached properly.
    - Creates a new FAQ object.
    - Retrieves the translation to check if caching works.
    - Asserts that the cached value matches the translated text.
    """
    faq = FAQ.objects.create(question="Capital of India", answer="<p>Delhi</p>")
    # Construct cache key for Hindi translation
    cache_key = f"faq_translation_{faq.id}_hi"

    # Retrieve translation to trigger caching
    # Call method to get translated question in Hindi
    translated_text = faq.get_translated_question("hi")
    cached_value = cache.get(cache_key)  # Retrieve the cached translation

    # Assert that the cached translation matches the translated text
    assert cached_value == translated_text
