from django.core.management.base import BaseCommand
from locations.models import Country, Region, City, Area


class Command(BaseCommand):
    help = 'Populate database with Cameroon locations'

    def handle(self, *args, **options):
        self.stdout.write('Starting Cameroon locations population...')

        # Create Cameroon
        cameroon, created = Country.objects.get_or_create(
            code='CMR',
            defaults={
                'name': 'Cameroon',
                'phone_code': '+237',
                'currency': 'XAF'
            }
        )

        if created:
            self.stdout.write(f'Created country: {cameroon.name}')
        else:
            self.stdout.write(f'Country already exists: {cameroon.name}')

        # Create Regions
        regions_data = [
            ('centre', 'Centre'),
            ('littoral', 'Littoral'),
            ('northwest', 'Northwest'),
            ('southwest', 'Southwest'),
        ]

        regions = {}
        for code, name in regions_data:
            region, created = Region.objects.get_or_create(
                code=code,
                country=cameroon,
                defaults={'name': name}
            )
            regions[code] = region
            if created:
                self.stdout.write(f'Created region: {region.name}')
            else:
                self.stdout.write(f'Region already exists: {region.name}')

        # Create Cities
        cities_data = [
            # Littoral Region
            {
                'name': 'Douala',
                'region': 'littoral',
                'is_major': True,
                'lat': 4.0511,
                'lng': 9.7679
            },

            # Centre Region
            {
                'name': 'Yaoundé',
                'region': 'centre',
                'is_major': True,
                'lat': 3.8480,
                'lng': 11.5021
            },

            # Northwest Region
            {
                'name': 'Bamenda',
                'region': 'northwest',
                'is_major': True,
                'lat': 5.9631,
                'lng': 10.1591
            },

            # Southwest Region
            {
                'name': 'Limbe',
                'region': 'southwest',
                'is_major': True,
                'lat': 4.0186,
                'lng': 9.2006
            },
            {
                'name': 'Buea',
                'region': 'southwest',
                'is_major': True,
                'lat': 4.1544,
                'lng': 9.2349
            },
        ]

        cities = {}
        for city_data in cities_data:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                region=regions[city_data['region']],
                defaults={
                    'is_major_city': city_data['is_major'],
                    'latitude': city_data['lat'],
                    'longitude': city_data['lng']
                }
            )
            cities[city_data['name']] = city
            if created:
                self.stdout.write(f'Created city: {city.name}')
            else:
                self.stdout.write(f'City already exists: {city.name}')

        # Create Areas/Quarters - All major neighborhoods in Cameroon cities
        areas_data = [
            # Douala Areas (Economic Capital)
            {'name': 'Akwa', 'city': 'Douala', 'is_commercial': True},
            {'name': 'Bonabéri', 'city': 'Douala'},
            {'name': 'Bonanjo', 'city': 'Douala', 'is_commercial': True},
            {'name': 'Bassa', 'city': 'Douala'},
            {'name': 'Deido', 'city': 'Douala'},
            {'name': 'New Bell', 'city': 'Douala'},
            {'name': 'Logpom', 'city': 'Douala'},
            {'name': 'Makepe', 'city': 'Douala'},
            {'name': 'Bonapriso', 'city': 'Douala', 'is_commercial': True},
            {'name': 'Kotto', 'city': 'Douala'},
            {'name': 'PK8', 'city': 'Douala'},
            {'name': 'PK12', 'city': 'Douala'},
            {'name': 'PK14', 'city': 'Douala'},
            {'name': 'PK17', 'city': 'Douala'},
            {'name': 'Ndogpassi', 'city': 'Douala'},
            {'name': 'Bépanda', 'city': 'Douala'},
            {'name': 'Cité SIC', 'city': 'Douala'},
            {'name': 'Kassalafam', 'city': 'Douala'},
            {'name': 'Yassa', 'city': 'Douala'},
            {'name': 'Japoma', 'city': 'Douala'},
            {'name': 'Ngangue', 'city': 'Douala'},
            {'name': 'Village', 'city': 'Douala'},
            {'name': 'Cite des Palmiers', 'city': 'Douala'},
            {'name': 'Bonamoussadi', 'city': 'Douala'},

            # Yaoundé Areas (Political Capital)
            {'name': 'Centre Ville', 'city': 'Yaoundé', 'is_commercial': True},
            {'name': 'Bastos', 'city': 'Yaoundé'},
            {'name': 'Melen', 'city': 'Yaoundé'},
            {'name': 'Kondengui', 'city': 'Yaoundé'},
            {'name': 'Emana', 'city': 'Yaoundé'},
            {'name': 'Obobogo', 'city': 'Yaoundé'},
            {'name': 'Nkol-Eton', 'city': 'Yaoundé'},
            {'name': 'Olézoa', 'city': 'Yaoundé'},
            {'name': 'Mimboman', 'city': 'Yaoundé'},
            {'name': 'Carrière', 'city': 'Yaoundé'},
            {'name': 'Mokolo', 'city': 'Yaoundé'},
            {'name': 'Mvog-Ada', 'city': 'Yaoundé'},
            {'name': 'Essos', 'city': 'Yaoundé'},
            {'name': 'Nsam', 'city': 'Yaoundé'},
            {'name': 'Mvog-Mbi', 'city': 'Yaoundé'},
            {'name': 'Ekounou', 'city': 'Yaoundé'},
            {'name': 'Etoug-Ebe', 'city': 'Yaoundé'},
            {'name': 'Biyem-Assi', 'city': 'Yaoundé'},
            {'name': 'Djoungolo', 'city': 'Yaoundé'},
            {'name': 'Nkomo', 'city': 'Yaoundé'},
            {'name': 'Simbock', 'city': 'Yaoundé'},
            {'name': 'Nkolbisson', 'city': 'Yaoundé'},

            # Bamenda Areas (Northwest Regional Capital)
            {'name': 'Commercial Avenue', 'city': 'Bamenda', 'is_commercial': True},
            {'name': 'Up Station', 'city': 'Bamenda'},
            {'name': 'Mile 4', 'city': 'Bamenda'},
            {'name': 'Ntarikon', 'city': 'Bamenda'},
            {'name': 'Mulang', 'city': 'Bamenda'},
            {'name': 'Nkwen', 'city': 'Bamenda'},
            {'name': 'Mankon', 'city': 'Bamenda'},
            {'name': 'Cow Street', 'city': 'Bamenda'},
            {'name': 'Foncha Street', 'city': 'Bamenda'},
            {'name': 'Food Market', 'city': 'Bamenda'},
            {'name': 'Old Town', 'city': 'Bamenda'},

            # Limbe Areas (Coastal City)
            {'name': 'Down Beach', 'city': 'Limbe'},
            {'name': 'Church Street', 'city': 'Limbe'},
            {'name': 'New Town', 'city': 'Limbe'},
            {'name': 'Mile 2', 'city': 'Limbe'},
            {'name': 'Mile 1', 'city': 'Limbe'},
            {'name': 'Batoke', 'city': 'Limbe'},
            {'name': 'Half Mile', 'city': 'Limbe'},
            {'name': 'Gardens', 'city': 'Limbe'},
            {'name': 'Checket', 'city': 'Limbe'},
            {'name': 'Motowo', 'city': 'Limbe'},

            # Buea Areas (University Town)
            {'name': 'Molyko', 'city': 'Buea'},
            {'name': 'Great Soppo', 'city': 'Buea'},
            {'name': 'Government Station', 'city': 'Buea'},
            {'name': 'Bonduma', 'city': 'Buea'},
            {'name': 'Mile 16', 'city': 'Buea'},
            {'name': 'Mile 15', 'city': 'Buea'},
            {'name': 'Mile 14', 'city': 'Buea'},
            {'name': 'Sandpit', 'city': 'Buea'},
            {'name': 'Bokwongo', 'city': 'Buea'},
            {'name': 'Lower Farms', 'city': 'Buea'},
            {'name': 'Upper Farms', 'city': 'Buea'},
            {'name': 'Clerks Quarters', 'city': 'Buea'},
        ]

        areas_created = 0
        areas_existing = 0

        for area_data in areas_data:
            city = cities[area_data['city']]
            area, created = Area.objects.get_or_create(
                name=area_data['name'],
                city=city,
                defaults={
                    'is_commercial': area_data.get('is_commercial', False),
                    'is_residential': True,
                    'has_tarred_roads': True if area_data.get('is_commercial') else False,
                    'has_electricity': True,
                    'has_water_supply': True,
                }
            )
            if created:
                areas_created += 1
                self.stdout.write(f'✓ Created area: {area.name}, {city.name}')
            else:
                areas_existing += 1

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(
                f'🎉 Successfully populated Cameroon locations!\n'
                f'📍 Country: Cameroon\n'
                f'🏛️  Regions: {len(regions_data)}\n'
                f'🏙️  Cities: {len(cities_data)}\n'
                f'🏘️  Areas: {areas_created} created, {areas_existing} already existed\n'
                f'📊 Total Areas: {areas_created + areas_existing}'
            )
        )
        self.stdout.write('='*50)

        # Display some examples
        self.stdout.write('\n📋 Sample locations created:')
        for city_name in ['Douala', 'Yaoundé']:
            city = cities[city_name]
            sample_areas = Area.objects.filter(city=city)[:3]
            self.stdout.write(f'  {city_name}: {", ".join([area.name for area in sample_areas])}...')

        self.stdout.write(f'\n✅ Ready for Property237.com! 🏠')