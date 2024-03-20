import csv
from django.core.management.base import BaseCommand
from user.models import College

class Command(BaseCommand):
    help = 'Populates the College table with college names from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing college names')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                college_name = row[1]  # Second column contains the college name

                # Check if the college already exists, if not create it
                college, created = College.objects.get_or_create(name=college_name)

                if created:
                    self.stdout.write(self.style.SUCCESS(f'College "{college.name}" imported successfully'))
                else:
                    self.stdout.write(self.style.WARNING(f'College "{college.name}" already exists'))
