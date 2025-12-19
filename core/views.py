from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import UploadFileForm, SignupForm
from .models import Upload, StoreProfile
from django.contrib.auth import login
from upload_data.models import UploadRecord

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    recent_uploads = []
    for r in UploadRecord.objects.filter(user=request.user).order_by('-uploaded_at')[:10]:
        recent_uploads.append({'name': r.file.name, 'uploaded_at': r.uploaded_at, 'source': 'new', 'id': r.id})
    for r in Upload.objects.filter(user=request.user).order_by('-uploaded_at')[:10]:
        recent_uploads.append({'name': r.file.name, 'uploaded_at': r.uploaded_at, 'source': 'legacy', 'id': r.id})
    recent_uploads = sorted(recent_uploads, key=lambda x: x['uploaded_at'], reverse=True)[:10]
    profile = getattr(request.user, 'store_profile', None)
    store_name = getattr(profile, 'store_name', '')
    return render(request, 'core/dashboard.html', {'user': request.user, 'recent_uploads': recent_uploads, 'store_name': store_name})

def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            obj = Upload(
                user=request.user,
                original_name=f.name,
                content_type=getattr(f, 'content_type', ''),
                size=getattr(f, 'size', 0),
            )
            obj.file.save(f.name, f, save=True)
            return redirect('dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'core/upload.html', {'form': form})

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            StoreProfile.objects.create(user=user, store_name=form.cleaned_data.get('store_name', ''))
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})
