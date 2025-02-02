from django.core.cache import cache
from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
import logging


logger = logging.getLogger("faqs")  # logger name


class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()  # Fix:Add parentheses
    question_hi = models.TextField(null=True, blank=True)
    question_bn = models.TextField(null=True, blank=True)

    def get_translated_question(self, lang):
        """Return cached translation if available,otherwise fetch&cache it."""
        cache_key = f"faq_translation_{self.id}_{lang}"
        cached_translation = cache.get(cache_key)

        if cached_translation:
            logger.info(f"Cache hit: {cache_key} -> {cached_translation}")
            return cached_translation  # Return cached translation
        # Fetch translation from database
        if lang == "hi" and self.question_hi:
            translation = self.question_hi
        elif lang == "bn" and self.question_bn:
            translation = self.question_bn
        else:
            # translation = self.question  # Default to English
            # Translate dynamically if no pre-stored translation
            translator = Translator()
            try:
                translation = translator.translate(self.question, dest=lang).text
                logger.info(f"Translated'{self.question}'to{lang}:{translation}")
            except Exception as e:
                logger.error(f"Translation failed: {e}")
                translation = self.question  # Fallback to original text

        # Store translation in cache
        cache.set(cache_key, translation, timeout=3600)

        # Check if caching worked
        logger.info(f"Cache set: {cache_key} -> {translation}")

        return translation

    def translate_text(self, text, target_language):
        """Translate the text to the specified target language."""
        try:
            translator = Translator()
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            logger.error(f"Error during translation: {e}")
            return text  # Fallback to original text if translation fails

    def save(self, *args, **kwargs):
        """Override save to automatically translate the question."""
        # Translate the question to Hindi and Bengali
        if not self.question_hi:
            self.question_hi = self.translate_text(self.question, 'hi')
        if not self.question_bn:
            self.question_bn = self.translate_text(self.question, 'bn')

        # Save the FAQ entry
        super().save(*args, **kwargs)
