from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment, Attachment
from .forms import TicketForm, AttachmentForm, CommentForm
from .decorators import admin_required, support_required, owner_required

# Create your views here.
def index(request):
    return render(request, 'tickets/index.html')  

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets_app/ticket_list.html', {'tickets': tickets})

@login_required
@owner_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'tickets_app/ticket_detail.html', {'ticket': ticket})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user  # Set the creator to the logged-in user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets_app/ticket_form.html', {'form': form})

@login_required
@admin_required  # Only admins can modify all ticket fields
def update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets_app/ticket_form.html', {'form': form})

@login_required
@support_required  # Only support staff can update ticket status
def update_ticket_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets_app/ticket_form.html', {'form': form})

@login_required
@admin_required  # Only admins can delete tickets
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    return redirect('ticket_list')

@login_required
@owner_required  # Only the ticket owner can add comments
def add_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()
    return render(request, 'tickets_app/add_comment.html', {'form': form, 'ticket': ticket})

@login_required
@owner_required  # Only the ticket owner can add attachments
def add_attachment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.ticket = ticket
            attachment.uploaded_by = request.user
            attachment.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = AttachmentForm()
    return render(request, 'tickets_app/add_attachment.html', {'form': form, 'ticket': ticket})

@login_required
@admin_required
def update_ticket(request, pk):
    # Only admin can modify everything
 pass  # Placeholder to avoid syntax error

@login_required
@support_required
def update_ticket_status(request, pk):
    # Only support can change status
 pass  # Placeholder to avoid syntax error

@login_required
@owner_required
def view_ticket(request, pk):
    # Only owner can view their ticket
 pass  # Placeholder to avoid syntax error