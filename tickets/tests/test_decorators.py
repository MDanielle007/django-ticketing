from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from tickets.models import Ticket

User = get_user_model()

class DecoratorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='regular', password='12345')
        self.admin = User.objects.create_user(username='admin', password='12345', is_staff=True)
        
        # Create support group and user
        self.support_group = Group.objects.create(name='support')
        self.support_user = User.objects.create_user(username='support', password='12345')
        self.support_user.groups.add(self.support_group)

        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )

    def test_admin_required_decorator(self):
        # Test with regular user
        self.client.login(username='regular', password='12345')
        response = self.client.get(reverse('update_ticket', kwargs={'pk': self.ticket.pk}))
        self.assertEqual(response.status_code, 403)

        # Test with admin user
        self.client.login(username='admin', password='12345')
        response = self.client.get(reverse('update_ticket', kwargs={'pk': self.ticket.pk}))
        self.assertEqual(response.status_code, 200)

    def test_support_required_decorator(self):
        # Test with regular user
        self.client.login(username='regular', password='12345')
        response = self.client.get(reverse('update_ticket_status', kwargs={'pk': self.ticket.pk}))
        self.assertEqual(response.status_code, 403)

        # Test with support user
        self.client.login(username='support', password='12345')
        response = self.client.get(reverse('update_ticket_status', kwargs={'pk': self.ticket.pk}))
        self.assertEqual(response.status_code, 200) 