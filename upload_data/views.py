from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .forms import UploadDataForm
from .models import UploadRecord
from core.models import Upload
from pathlib import Path
import pandas as pd

@login_required
def upload_sales(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            rec = UploadRecord(user=request.user)
            rec.file.save(f.name, f, save=True)
            return redirect('dashboard')
    else:
        form = UploadDataForm()
    return render(request, 'upload_data/upload.html', {'form': form})

@login_required
def upload_history(request: HttpRequest) -> HttpResponse:
    items = []
    for r in UploadRecord.objects.filter(user=request.user).order_by('-uploaded_at'):
        items.append({
            'name': r.file.name,
            'uploaded_at': r.uploaded_at,
            'url': getattr(r.file, 'url', ''),
            'source': 'new',
            'id': r.id,
        })
    for r in Upload.objects.filter(user=request.user).order_by('-uploaded_at'):
        items.append({
            'name': r.file.name,
            'uploaded_at': r.uploaded_at,
            'url': getattr(r.file, 'url', ''),
            'source': 'legacy',
            'id': r.id,
        })
    items = sorted(items, key=lambda x: x['uploaded_at'], reverse=True)
    return render(request, 'upload_data/history.html', {'items': items})

@login_required
def view_upload(request: HttpRequest, source: str, pk: int) -> HttpResponse:
    if source == 'new':
        rec = get_object_or_404(UploadRecord, pk=pk, user=request.user)
        path_str = rec.file.path
        uploaded_at = rec.uploaded_at
        name = rec.file.name
        file_url = getattr(rec.file, 'url', '')
    else:
        rec = get_object_or_404(Upload, pk=pk, user=request.user)
        path_str = rec.file.path
        uploaded_at = rec.uploaded_at
        name = rec.file.name
        file_url = getattr(rec.file, 'url', '')
    p = Path(path_str)
    df = None
    if p.suffix.lower() == '.csv':
        df = pd.read_csv(p, dtype=str)
    else:
        df = pd.read_excel(p, engine='openpyxl', dtype=str)
    df = df.head(200)
    table_html = df.to_html(classes='table table-striped table-sm', index=False, border=0)
    return render(request, 'upload_data/view_file.html', {
        'name': name,
        'uploaded_at': uploaded_at,
        'table_html': table_html,
        'file_url': file_url,
    })
