from django.core.management.base import BaseCommand
from properties.models import PropertyType, PropertyStatus


class Command(BaseCommand):
    help = 'Populate database with property types and statuses'

    def handle(self, *args, **options):
        self.stdout.write('Starting property types and statuses population...')

        # Property Types Data (name, category)
        property_types_data = [
            ('Chambre Modern', 'chambre_modern'),
            ('Studio', 'studio'),
            ('Apartment', 'apartment'),
            ('Bungalow', 'bungalow'),
            ('Villa', 'villa_duplex'),
            ('Duplex', 'villa_duplex'),
            ('Commercial Office', 'commercial'),
            ('Shop', 'commercial'),
            ('Warehouse', 'warehouse'),
            ('Guest House', 'guest_house'),
            ('Land', 'land'),
        ]

        # Create Property Types
        for name, category in property_types_data:
            property_type, created = PropertyType.objects.get_or_create(
                name=name,
                defaults={'category': category}
            )
            if created:
                self.stdout.write(f'Created property type: {property_type.name}')
            else:
                self.stdout.write(f'Property type already exists: {property_type.name}')

        # Property Status Data
        property_statuses_data = [
            'available',
            'pending',
            'sold',
            'rented',
            'withdrawn',
            'under_offer',
        ]

        # Create Property Statuses
        for status_name in property_statuses_data:
            property_status, created = PropertyStatus.objects.get_or_create(
                name=status_name
            )
            if created:
                self.stdout.write(f'Created property status: {property_status.get_name_display()}')
            else:
                self.stdout.write(f'Property status already exists: {property_status.get_name_display()}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {len(property_types_data)} property types '
                f'and {len(property_statuses_data)} property statuses'
            )
        )