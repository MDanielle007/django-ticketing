from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from tickets.models import Ticket, Comment, Attachment, ActivityLog, TicketStatusHistory

User = get_user_model()

# Model Tests
class TicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            priority='medium',
            status='open',
            created_by=self.user
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.title, 'Test Ticket')
        self.assertEqual(self.ticket.status, 'open')
        self.assertEqual(self.ticket.created_by, self.user)

    def test_ticket_str_representation(self):
        self.assertEqual(str(self.ticket), 'Test Ticket')

# View Tests
class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_user(username='admin', password='12345', is_staff=True)
        
        self.support_group = Group.objects.create(name='support')
        self.support_user = User.objects.create_user(username='support', password='12345')
        self.support_user.groups.add(self.support_group)

        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )

    def test_ticket_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/index.html')

# Decorator Tests
class DecoratorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='regular', password='12345')
        self.admin = User.objects.create_user(username='admin', password='12345', is_staff=True)
        
        self.support_group = Group.objects.create(name='support')
        self.support_user = User.objects.create_user(username='support', password='12345')
        self.support_user.groups.add(self.support_group)

        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )

    def test_admin_required_decorator(self):
        self.client.login(username='regular', password='12345')
        response = self.client.get(reverse('update_ticket', kwargs={'pk': self.ticket.pk}))
        self.assertEqual(response.status_code, 403)

# Signal Tests
class SignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.support_group = Group.objects.create(name='Support')
        self.support_user = User.objects.create_user(username='support', password='12345')
        self.support_user.groups.add(self.support_group)

    def test_ticket_status_change_logging(self):
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            status='open',
            created_by=self.user,
            updated_by=self.user
        )

        ticket.status = 'in_progress'
        ticket.save()

        status_history = TicketStatusHistory.objects.filter(ticket=ticket)
        self.assertEqual(status_history.count(), 1)
