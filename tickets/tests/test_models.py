from django.test import TestCase
from django.contrib.auth import get_user_model
from tickets.models import Ticket, Comment, Attachment, ActivityLog, TicketStatusHistory

User = get_user_model()

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

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )
        self.comment = Comment.objects.create(
            ticket=self.ticket,
            user=self.user,
            message='Test Comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.message, 'Test Comment')
        self.assertEqual(self.comment.user, self.user) 