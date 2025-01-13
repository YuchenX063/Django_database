import os
import csv
from django.core.management.base import BaseCommand
from database.models import Church, Person, Church_Person, Small_Church, Church_Church

class Command(BaseCommand):
    help = 'Import data from CSV files'

    def handle(self, *args, **kwargs):
        self.rec_church = set()
        self.rec_person = set()
        self.rec_small_church = set()
        self.rec_church_person = set()
        self.rec_church_church = set()

        folder_path = 'D:\\python\\Django\\data'
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

        for file in files:
            file_path = os.path.join(folder_path, file)
            print(f"Processing file: {file_path}")
            self.import_data(file_path)

    def import_data(self, file_path):
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            df = list(reader)
            print(f"Read {len(df)} rows from {file_path}")
            if df:
                print("First row:", df[0])

        church_keys = ['instID', 'year', 'church_type', 'instName', 'language', 'instNote', 'placeName', 'region', 'state_orig', 'city_reg', 'latitude', 'longitude', 'attendingInstID', 'memberType', 'member', 'affiliated', 'diocese']
        small_church_keys = ['instID', 'year', 'church_type', 'instName', 'language', 'instNote', 'placeName', 'region', 'state_orig', 'city_reg', 'latitude', 'longitude', 'attendingInstID', 'attendingChurch', 'attendingChurchFrequency', 'diocese']
        person_keys = ['persID', 'year', 'persTitle', 'persName', 'persSuffix', 'persNote']
        church_person_keys = ['instID', 'persID', 'year', 'persTitle', 'persName']
        church_church_keys = ['instID', 'attendingInstID', 'year']

        # Strip BOM from values
        for row in df:
            for key in row:
                row[key] = row[key].lstrip('\ufeff')

        # Convert year values to integers
        for row in df:
            try:
                row['year'] = int(float(row['year']))
            except ValueError:
                print(f"Invalid year value: {row['year']}")
                continue

        # Filter and import church data
        church_info = [{key: row[key] for key in church_keys if key in row} for row in df]
        print(f"Found {len(church_info)} church records")
        for item in church_info:
            temp = (item['instID'], item['year'])
            if temp not in self.rec_church and not item['attendingInstID']:
                self.rec_church.add(temp)
                church, created = Church.objects.get_or_create(**item)
                if created:
                    print(f"Created Church instance: {item}")

        # Filter and import person data
        person_info = [{key: row[key] for key in person_keys if key in row} for row in df]
        print(f"Found {len(person_info)} person records")
        for item in person_info:
            temp = (item['persID'], item['year'])
            if temp not in self.rec_person and item['persID']:
                if not item['persID']:  # Check if persID has a value
                    print(f"Skipping Person instance due to missing persID: {item}")
                    continue
                self.rec_person.add(temp)
                person, created = Person.objects.get_or_create(**item)
                if created:
                    print(f"Created Person instance: {item}")

        # Filter and import small church data
        small_church_info = [{key: row[key] for key in small_church_keys if key in row} for row in df]
        print(f"Found {len(small_church_info)} small church records")
        for item in small_church_info:
            temp = (item['instID'], item['year'])
            if temp not in self.rec_small_church and item['attendingInstID']:
                self.rec_small_church.add(temp)
                small_church, created = Small_Church.objects.get_or_create(**item)
                if created:
                    print(f"Created Small_Church instance: {item}")

        # Filter and import church-person data
        church_person_info = [{key: row[key] for key in church_person_keys if key in row} for row in df]
        print(f"Found {len(church_person_info)} church-person records")
        for item in church_person_info:
            temp = (item['instID'], item['persID'], item['year'])
            #print(f"Processing Church_Person instance: {item}")
            if temp not in self.rec_church_person and item['persID']:
                self.rec_church_person.add(temp)
                print(item['instID'], item['persID'], item['year'])
                try:
                    church = Church.objects.get(instID=item['instID'], year=item['year'])
                except Church.DoesNotExist:
                    print(f"Church with instID {item['instID']} and year {item['year']} does not exist. Skipping.")
                    continue
                person = Person.objects.get(persID=item['persID'], year=item['year'])
                church_person, created = Church_Person.objects.get_or_create(
                    instID=church.instID,
                    persID=person.persID,
                    year_church=church.year,
                    year_person=person.year,
                    persTitle=item['persTitle'],
                    persName=item['persName'],
                    person_church=church,
                    person=person
                )
                if created:
                    print(f"Created Church_Person instance: {item}")

        # Filter and import church-church data
        church_church_info = [{key: row[key] for key in church_church_keys if key in row} for row in df]
        print(f"Found {len(church_church_info)} church-church records")
        for item in church_church_info:
            temp = (item['instID'], item['attendingInstID'], item['year'])
            if temp not in self.rec_church_church and item['attendingInstID']:
                self.rec_church_church.add(temp)
                #print(f"Processing Church_Church instance: {item}")
                try:
                    church = Church.objects.get(instID=item['attendingInstID'], year=item['year'])
                except Church.DoesNotExist:
                    print(f"Church with instID {item['instID']} and year {item['year']} does not exist.")
                    continue
                try:
                    attending_church = Small_Church.objects.get(instID=item['instID'], year=item['year'])
                except Small_Church.DoesNotExist:
                    print(f"Attending Church with instID {item['attendingInstID']} and year {item['year']} does not exist.")
                    continue
                church_church, created = Church_Church.objects.get_or_create(
                    instID=church.instID,
                    attendingInstID=attending_church.instID,
                    year_church=church.year,
                    year_small_church=attending_church.year,
                    church=church,
                    small_church=attending_church
                )
                if created:
                    print(f"Created Church_Church instance: {item}")