from django import forms
from .models import Ticket
from .models import Comment
from .models import Attachment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'status', 'assigned_to']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file_name', 'file_path']