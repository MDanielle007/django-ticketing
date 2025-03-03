from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Ticket, ActivityLog, TicketStatusHistory

@receiver(pre_save, sender=Ticket)
def log_ticket_changes(sender, instance, **kwargs):
    """
    Logs changes to ticket fields (title, description, priority, status) in ActivityLog.
    Logs status changes separately in TicketStatusHistory.
    Auto-assigns ticket to the least busy Support user if assigned_to is empty.
    """
    if instance.pk:  # Only try to get old ticket if this is an update, not a creation
        try:
            old_ticket = Ticket.objects.get(pk=instance.pk)
            changes = []

            # Track field changes and log them
            if old_ticket.title != instance.title:
                changes.append(f"Title changed from '{old_ticket.title}' to '{instance.title}'")
            if old_ticket.description != instance.description:
                changes.append("Description updated")
            if old_ticket.priority != instance.priority:
                changes.append(f"Priority changed from {old_ticket.priority} to {instance.priority}")
            if old_ticket.status != instance.status:
                changes.append(f"Status changed from {old_ticket.status} to {instance.status}")
                
                # Log status change in TicketStatusHistory
                if instance.updated_by:  # Only log if we know who made the change
                    TicketStatusHistory.objects.create(
                        ticket=instance,
                        changed_by=instance.updated_by,
                        old_status=old_ticket.status,
                        new_status=instance.status
                    )

            # Save changes in ActivityLog
            if changes and instance.updated_by:
                ActivityLog.objects.create(
                    ticket=instance,
                    user=instance.updated_by,
                    action="; ".join(changes)
                )
        except Ticket.DoesNotExist:
            pass  # Skip logging for new tickets
    
    # Auto-assign ticket to the least busy support agent if none is assigned
    if not instance.assigned_to:
        assign_ticket_to_support(instance)

def assign_ticket_to_support(ticket):
    """
    Finds the Support user with the fewest assigned tickets and assigns the ticket.
    If no Support users are available, the ticket remains unassigned.
    """
    try:
        support_group = Group.objects.get(name='Support')
        support_users = support_group.user_set.all()
        
        if support_users.exists():
            # Find the least busy support agent (fewest assigned tickets)
            least_busy_agent = min(support_users, key=lambda user: user.assigned_tickets.count(), default=None)
            if least_busy_agent:
                ticket.assigned_to = least_busy_agent
    except Group.DoesNotExist:
        pass  # Skip auto-assignment if Support group doesn't exist
