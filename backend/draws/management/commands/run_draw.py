import random
from collections import Counter
from datetime import date
from django.core.management.base import BaseCommand
from django.utils import timezone
from scores.models import Score
from draws.models import DrawResult


class Command(BaseCommand):
    help = "Simulate (not publish) this month's draw: random or weighted-by-frequency."

    def add_arguments(self, parser):
        parser.add_argument("--method", choices=["random", "weighted"], default="random")

    def handle(self, *args, **options):
        method = options["method"]
        today = timezone.now().date()
        month_start = date(today.year, today.month, 1)

        if method == "random":
            numbers = random.sample(range(1, 46), 5)
        else:
            freq = Counter(Score.objects.values_list("value", flat=True))
            if not freq:
                numbers = random.sample(range(1, 46), 5)
            else:
                population = list(range(1, 46))
                weights = [freq.get(n, 0) + 1 for n in population]  # +1 so unseen numbers stay possible
                numbers = []
                pool = list(zip(population, weights))
                for _ in range(5):
                    total = sum(w for _, w in pool)
                    r = random.uniform(0, total)
                    upto = 0
                    for i, (n, w) in enumerate(pool):
                        upto += w
                        if upto >= r:
                            numbers.append(n)
                            pool.pop(i)
                            break

        draw, created = DrawResult.objects.get_or_create(
            month=month_start,
            defaults={"winning_numbers": sorted(numbers), "method": method},
        )
        if not created:
            self.stdout.write(self.style.WARNING(f"Draw for {month_start} already exists (simulated or published)."))
            return

        self.stdout.write(self.style.SUCCESS(
            f"Simulated {method} draw for {month_start}: {sorted(numbers)}. "
            f"Review in /admin/draws/drawresult/ and use the 'Publish' action to finalize."
        ))
