from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from .forms import (
    VolunteerSignupForm, VeteranSignupForm,
    HelpRequestForm, ApplicationForm
)
from .models import HelpRequest, Application
from django.core.exceptions import ValidationError

def check_rate_limit(user_id, action, max_requests=5, period=300):
    """
    Rate limiting: max_requests за period секунд
    """
    cache_key = f"rate_limit_{action}_{user_id}"
    now = datetime.now()
    requests = cache.get(cache_key, [])
    
    # Удаляем старые запросы
    requests = [time for time in requests if time > now - timedelta(seconds=period)]
    
    if len(requests) >= max_requests:
        return False
        
    requests.append(now)
    cache.set(cache_key, requests, period)
    return True

def signup_volunteer(request):
    if request.method == 'POST':
        form = VolunteerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('request_list')
    else:
        form = VolunteerSignupForm()
    return render(request, 'core/signup.html', {'form': form, 'role': 'Волонтёр'})

def signup_veteran(request):
    if request.method == 'POST':
        form = VeteranSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('request_list')
    else:
        form = VeteranSignupForm()
    return render(request, 'core/signup.html', {'form': form, 'role': 'Ветеран'})

@login_required
def request_list(request):
    qs = HelpRequest.objects.exclude(status='done')
    ht = request.GET.get('help_type')
    loc= request.GET.get('location')
    if ht:
        qs = qs.filter(help_type=ht)
    if loc:
        qs = qs.filter(location__icontains=loc)
    return render(request, 'core/request_list.html', {'requests': qs})

@login_required
def request_detail(request, pk):
    hr = get_object_or_404(HelpRequest, pk=pk)
    return render(request, 'core/request_detail.html', {'request_obj': hr})

@login_required
@user_passes_test(lambda u: u.is_veteran())
def create_request(request):
    if request.method == 'POST':
        if not check_rate_limit(request.user.id, 'create_request', max_requests=3, period=3600):
            return HttpResponseForbidden('Превышен лимит создания заявок. Попробуйте позже.')
            
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            hr = form.save(commit=False)
            hr.veteran = request.user
            try:
                hr.full_clean()  # Вызываем валидацию модели
                hr.save()
                return redirect('dashboard')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = HelpRequestForm()
    return render(request, 'core/respond.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_veteran())
def dashboard(request):
    qs = HelpRequest.objects.filter(veteran=request.user)
    return render(request, 'core/dashboard.html', {'requests': qs})

@login_required
@user_passes_test(lambda u: u.is_veteran())
def revoke_request(request, pk):
    hr = get_object_or_404(HelpRequest, pk=pk, veteran=request.user)
    hr.delete()
    return redirect('dashboard')

@login_required
@user_passes_test(lambda u: u.is_volunteer())
def respond_request(request, pk):
    hr = get_object_or_404(HelpRequest, pk=pk)
    if request.method == 'POST':
        if not check_rate_limit(request.user.id, 'respond_request', max_requests=5, period=3600):
            return HttpResponseForbidden('Превышен лимит откликов. Попробуйте позже.')
            
        form = ApplicationForm(request.POST)
        # Create instance but don't save to DB yet
        app = form.save(commit=False)
        # Set required relationships
        app.volunteer = request.user
        app.help_request = hr
        
        # Now validate the form with all relationships set
        if form.is_valid():
            try:
                app.full_clean()  # Validate the model
                app.save()
                return redirect('request_detail', pk=pk)
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = ApplicationForm()
    return render(request, 'core/respond.html', {
        'form': form, 'request_obj': hr
    })

@login_required
@user_passes_test(lambda u: u.is_veteran())
def update_status(request, pk):
    hr = get_object_or_404(HelpRequest, pk=pk, veteran=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(HelpRequest.STATUS_CHOICES):
            hr.status = new_status
            hr.save()
            return redirect('dashboard')
    return render(request, 'core/update_status.html', {
        'request_obj': hr,
        'choices':     HelpRequest.STATUS_CHOICES
    })