from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import LeaveRequest, LeaveType
from .forms import LeaveRequestForm, LeaveTypeForm


def is_hr(user):
    return user.is_authenticated and user.is_hr


@login_required
def leave_request_list(request):
    if request.user.is_hr:
        leaves = LeaveRequest.objects.all().order_by('-date_requested')
    else:
        leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-date_requested')
    return render(request, 'leaves/leave_request_list.html', {'leaves': leaves})


@login_required
def leave_request_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leaves/leave_form.html', {'form': form})


@login_required
@user_passes_test(is_hr)
def leave_request_approve(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'A'
    leave.approved_by = request.user
    leave.save()
    messages.success(request, 'Leave approved successfully!')
    return redirect('leave_list')


@login_required
@user_passes_test(is_hr)
def leave_request_reject(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'R'
    leave.approved_by = request.user
    leave.save()
    messages.success(request, 'Leave rejected successfully!')
    return redirect('leave_list')


# LeaveType Views
class LeaveTypeListView(ListView):
    model = LeaveType
    template_name = 'leaves/leave_type_list.html'
    context_object_name = 'leavetypes'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr:
            messages.error(request, 'You are not authorized to view leave types.')
            return redirect('leave_list')
        return super().dispatch(request, *args, **kwargs)


class LeaveTypeCreateView(CreateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leavetype_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr:
            messages.error(request, 'You are not authorized to create leave types.')
            return redirect('leave_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Leave type created successfully!')
        return super().form_valid(form)


class LeaveTypeUpdateView(UpdateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leavetype_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr:
            messages.error(request, 'You are not authorized to update leave types.')
            return redirect('leave_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Leave type updated successfully!')
        return super().form_valid(form)


class LeaveTypeDeleteView(DeleteView):
    model = LeaveType
    template_name = 'leaves/leave_confirm_delete.html'
    success_url = reverse_lazy('leavetype_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_hr:
            messages.error(request, 'You are not authorized to delete leave types.')
            return redirect('leave_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Leave type deleted successfully!')
        return super().delete(request, *args, **kwargs)

