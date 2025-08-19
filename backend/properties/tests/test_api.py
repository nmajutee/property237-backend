from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from properties.models import Property, PropertyType, PropertyStatus
from locations.models import Country, Region, City, Area
from agentprofile.models import AgentProfile

User = get_user_model()


class PropertyAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='agent'
        )

        # Create agent profile
        self.agent_profile = AgentProfile.objects.create(
            user=self.user,
            license_number='TEST123',
            agency_name='Test Agency'
        )

        # Create location hierarchy
        self.country = Country.objects.create(name='Cameroon', code='CM')
        self.region = Region.objects.create(name='Centre', country=self.country)
        self.city = City.objects.create(name='Yaoundé', region=self.region)
        self.area = Area.objects.create(name='Bastos', city=self.city)

        # Create property metadata
        self.property_type = PropertyType.objects.create(
            name='Studio', category='residential'
        )
        self.property_status = PropertyStatus.objects.create(
            name='Available'
        )

        # Create test property
        self.property = Property.objects.create(
            title='Test Property',
            property_type=self.property_type,
            status=self.property_status,
            listing_type='rent',
            price=150000,
            currency='XAF',
            area=self.area,
            agent=self.agent_profile,
            description='Test property description'
        )

        self.client = APIClient()

    def test_property_list_api(self):
        """Test property list endpoint"""
        url = reverse('properties:property-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Property')

    def test_property_detail_api(self):
        """Test property detail endpoint"""
        url = reverse('properties:property-detail', kwargs={'slug': self.property.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Property')

    def test_property_create_api_authenticated(self):
        """Test property creation with authentication"""
        self.client.force_authenticate(user=self.user)

        url = reverse('properties:property-list-create')
        data = {
            'title': 'New Test Property',
            'property_type': self.property_type.id,
            'status': self.property_status.id,
            'listing_type': 'sale',
            'price': 200000,
            'currency': 'XAF',
            'area': self.area.id,
            'description': 'New test property'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_property_create_api_unauthenticated(self):
        """Test property creation without authentication"""
        url = reverse('properties:property-list-create')
        data = {
            'title': 'New Test Property',
            'property_type': self.property_type.id,
            'status': self.property_status.id,
            'listing_type': 'sale',
            'price': 200000
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_property_filter_by_price(self):
        """Test property filtering by price"""
        url = reverse('properties:property-list-create')
        response = self.client.get(url, {'price_min': 100000, 'price_max': 200000})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_property_search(self):
        """Test property search"""
        url = reverse('properties:property-list-create')
        response = self.client.get(url, {'search': 'Test'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)