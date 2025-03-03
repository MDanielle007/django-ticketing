from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from tickets.models import Ticket

User = get_user_model()

class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_user(username='admin', password='12345', is_staff=True)
        
        # Create support group and add a support user
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
        self.assertTemplateUsed(response, 'tickets_app/ticket_list.html')

    def test_ticket_detail_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ticket_detail', kwargs={'pk': self.ticket.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets_app/ticket_detail.html')

    def test_create_ticket_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create_ticket'), {
            'title': 'New Ticket',
            'description': 'New Description',
            'priority': 'medium',
            'status': 'open'
        })
        self.assertEqual(Ticket.objects.count(), 2) 