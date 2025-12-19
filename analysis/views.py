from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from upload_data.models import UploadRecord
from core.models import Upload
from .utils import read_upload_to_df, clean_df, add_calculations, compute_analytics
from pathlib import Path

@login_required
def analyze_latest(request: HttpRequest) -> HttpResponse:
    rec = UploadRecord.objects.filter(user=request.user).order_by('-uploaded_at').first()
    path_str = None
    file_name = None
    uploaded_at = None
    source = None
    if rec:
        path_str = rec.file.path
        file_name = rec.file.name
        uploaded_at = rec.uploaded_at
        source = 'new'
    else:
        rec2 = Upload.objects.filter(user=request.user).order_by('-uploaded_at').first()
        if rec2:
            path_str = rec2.file.path
            file_name = rec2.file.name
            uploaded_at = rec2.uploaded_at
            source = 'legacy'
        else:
            return JsonResponse({'error': 'No uploaded file found for user'}, status=404)
    p = Path(path_str)
    try:
        df = read_upload_to_df(str(p))
        df = clean_df(df)
        df = add_calculations(df)
        results = compute_analytics(df)
        meta = {
            'file': {'name': file_name, 'uploaded_at': str(uploaded_at), 'source': source},
            'shape': {'rows': int(df.shape[0]), 'columns': int(df.shape[1])},
        }
        return JsonResponse({'status': 'ok', 'results': results, 'meta': meta})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def analysis_dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'analysis/dashboard.html')

@login_required
def analyze_file(request: HttpRequest, source: str, pk: int) -> HttpResponse:
    path_str = None
    file_name = None
    uploaded_at = None
    src = None
    if source == 'new':
        rec = UploadRecord.objects.filter(user=request.user, pk=pk).first()
        if rec:
            path_str = rec.file.path
            file_name = rec.file.name
            uploaded_at = rec.uploaded_at
            src = 'new'
    elif source == 'legacy':
        rec = Upload.objects.filter(user=request.user, pk=pk).first()
        if rec:
            path_str = rec.file.path
            file_name = rec.file.name
            uploaded_at = rec.uploaded_at
            src = 'legacy'
    if not path_str:
        return JsonResponse({'error': 'File not found for user'}, status=404)
    p = Path(path_str)
    try:
        df = read_upload_to_df(str(p))
        df = clean_df(df)
        df = add_calculations(df)
        results = compute_analytics(df)
        meta = {
            'file': {'name': file_name, 'uploaded_at': str(uploaded_at), 'source': src},
            'shape': {'rows': int(df.shape[0]), 'columns': int(df.shape[1])},
        }
        return JsonResponse({'status': 'ok', 'results': results, 'meta': meta})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
