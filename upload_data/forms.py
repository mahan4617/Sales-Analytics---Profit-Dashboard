from django import forms
from pathlib import Path

ALLOWED_EXTS = {'.csv', '.xlsx'}
ALLOWED_CT = {
    'text/csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}

class UploadDataForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        f = self.cleaned_data['file']
        ext = Path(f.name).suffix.lower()
        if ext not in ALLOWED_EXTS:
            raise forms.ValidationError('Only CSV or Excel (.xlsx) files are allowed.')
        ct = getattr(f, 'content_type', '')
        if not (ct in ALLOWED_CT or (ct.startswith('text/') and ext == '.csv')):
            raise forms.ValidationError('Invalid file type.')
        if getattr(f, 'size', 0) > 10 * 1024 * 1024:
            raise forms.ValidationError('File too large (max 10MB).')
        return f
