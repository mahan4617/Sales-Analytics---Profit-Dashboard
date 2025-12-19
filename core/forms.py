from django import forms
from pathlib import Path
from django.contrib.auth.forms import UserCreationForm

ALLOWED_EXTS = {'.csv', '.xlsx', '.xls'}
ALLOWED_CT = {
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        f = self.cleaned_data['file']
        ext = Path(f.name).suffix.lower()
        if ext not in ALLOWED_EXTS:
            raise forms.ValidationError('Only CSV or Excel files are allowed.')
        ct = getattr(f, 'content_type', '')
        size = getattr(f, 'size', 0)
        if not (ct in ALLOWED_CT or (ct.startswith('text/') and ext == '.csv')):
            raise forms.ValidationError('Invalid file type.')
        if size > 10 * 1024 * 1024:
            raise forms.ValidationError('File too large (max 10MB).')
        return f

class SignupForm(UserCreationForm):
    store_name = forms.CharField(max_length=255)
