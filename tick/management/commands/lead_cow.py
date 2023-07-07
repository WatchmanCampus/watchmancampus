from django.core.management.base import BaseCommand
from tick.models import Institution
from mysite.fixtures.institutions import data

class Command(BaseCommand):
    help = 'Load institutions into the database'

    def handle(self, *args, **options):
        for item in data:
            for state, schools in item.items():
                for value, school in schools.items():
                    institution = Institution(state=state, school=school)
                    institution.save()
        self.stdout.write(self.style.SUCCESS('Institutions loaded successfully.'))