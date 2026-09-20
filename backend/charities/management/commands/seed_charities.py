from django.core.management.base import BaseCommand
from charities.models import Charity


class Command(BaseCommand):
    help = "Seed a handful of sample charities so the platform isn't empty on first deploy."

    def handle(self, *args, **options):
        samples = [
            {"name": "Greenfield Youth Trust", "tagline": "Sport access for kids who'd otherwise have none",
             "description": "Funds junior golf and sport programs in underserved communities.",
             "is_featured": True},
            {"name": "Fairway Forward Foundation", "tagline": "Rebuilding lives through mentorship",
             "description": "Mentorship and job-readiness programs for at-risk youth.",
             "is_featured": True},
            {"name": "Clear Water Initiative", "tagline": "Clean water, healthier communities",
             "description": "Builds water access infrastructure in rural regions."},
            {"name": "Veterans Bridge Fund", "tagline": "Supporting those who served",
             "description": "Transition support and mental health resources for veterans."},
        ]
        for s in samples:
            obj, created = Charity.objects.get_or_create(name=s["name"], defaults=s)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: {obj.name}"))
