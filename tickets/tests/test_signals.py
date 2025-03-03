from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from tickets.models import Ticket, ActivityLog, TicketStatusHistory

User = get_user_model()

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
            updated_by=self.user  # Make sure to set this in your views
        )

        # Change ticket status
        ticket.status = 'in_progress'
        ticket.save()

        # Check if status history was created
        status_history = TicketStatusHistory.objects.filter(ticket=ticket)
        self.assertEqual(status_history.count(), 1)
        self.assertEqual(status_history.first().old_status, 'open')
        self.assertEqual(status_history.first().new_status, 'in_progress')

    def test_activity_log_creation(self):
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user,
            updated_by=self.user
        )

        # Make some changes
        ticket.title = 'Updated Title'
        ticket.priority = 'high'
        ticket.save()

        # Check if activity was logged
        activity_logs = ActivityLog.objects.filter(ticket=ticket)
        self.assertTrue(activity_logs.exists()) 