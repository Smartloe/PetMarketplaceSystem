from django.core.management.base import BaseCommand

from charts.demo_seed import seed_demo_business_data


class Command(BaseCommand):
    help = "Seed demo business records for admin analytics"

    def handle(self, *args, **options):
        summary = seed_demo_business_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded users={summary.users} products={summary.products} orders={summary.orders}"
            )
        )
