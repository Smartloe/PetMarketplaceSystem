from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from charts.demo_seed import seed_demo_business_data


class Command(BaseCommand):
    help = "Seed demo business records for admin analytics"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                "seed_demo_business_data can only run when DEBUG=True."
            )
        summary = seed_demo_business_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded users={summary.users} products={summary.products} orders={summary.orders}"
            )
        )
