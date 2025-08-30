# backups/forms.py

from django import forms

class RestoreForm(forms.Form):
    dump_file = forms.FileField(
        label="Archivo de respaldo (.dump)",
        help_text="Selecciona el archivo .dump generado previamente"
    )
