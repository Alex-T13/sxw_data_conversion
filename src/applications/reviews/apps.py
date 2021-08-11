from django.apps import AppConfig


class ReviewConfig(AppConfig):
    label = 'reviews'
    name = f"applications.{label}"
