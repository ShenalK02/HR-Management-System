from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Announcement
from .forms import AnnouncementForm
from django.db.models import Q

@login_required
def announcement_list(request):
    # Get unexpired announcements or those without expiry date
    today = timezone.now().date()
    announcements = Announcement.objects.filter(
    Q(expiry_date__gte=today) | Q(expiry_date__isnull=True)
    )
    
    # Sort by importance first, then by date
    announcements = announcements.order_by('-is_important', '-created_at')
    
    return render(request, 'announcements/announcement_list.html', {
        'announcements': announcements
    })

@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcements/announcement_detail.html', {
        'announcement': announcement
    })

@login_required
def announcement_create(request):
    # Only HR can create announcements
    if not request.user.is_hr:
        messages.error(request, "You don't have permission to create announcements.")
        return redirect('announcement_list')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, "Announcement created successfully!")
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/announcement_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def announcement_edit(request, pk):
    # Only HR can edit announcements
    if not request.user.is_hr:
        messages.error(request, "You don't have permission to edit announcements.")
        return redirect('announcement_list')
    
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully!")
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'announcements/announcement_form.html', {
        'form': form,
        'action': 'Update'
    })

@login_required
def announcement_delete(request, pk):
    # Only HR can delete announcements
    if not request.user.is_hr:
        messages.error(request, "You don't have permission to delete announcements.")
        return redirect('announcement_list')
    
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, "Announcement deleted successfully!")
        return redirect('announcement_list')
    
    return render(request, 'announcements/announcement_confirm_delete.html', {
        'announcement': announcement
    })
