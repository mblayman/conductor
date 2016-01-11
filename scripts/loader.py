import csv
from django.db.utils import IntegrityError
from django.utils.text import slugify
from planner.models import School


School.objects.all().delete()

with open('universities.csv', 'r') as f:
    rows = csv.reader(f)
    counter = 0
    for row in rows:
        counter += 1
        created = True
        try:
            silent = School.objects.create(
                name=row[0], url=row[1], slug=slugify(row[0]))
        except IntegrityError:
            created = False
        if not created:
            print('Failed', row[0], row[1], slugify(row[0]))
            silent = School.objects.create(
                name=row[0], url=row[1],
                slug='{}-{}'.format(slugify(row[0]), counter))

