from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import StreamingHttpResponse
import shlex, subprocess, os
from tempfile import NamedTemporaryFile
from backups.utils import get_pg_connection
from .forms import RestoreForm

@staff_member_required
def descargar_backup(request):
    db_url, env = get_pg_connection()
    cmd = f"pg_dump --format=custom --dbname={db_url}"
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, env=env)
    filename = f"backup_{db_url.split('/')[-1]}.dump"
    response = StreamingHttpResponse(proc.stdout, content_type="application/octet-stream")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@staff_member_required
def restaurar_backup(request):
    form = RestoreForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        # Guardar dump en archivo temporal
        tmp_path = None
        try:
            with NamedTemporaryFile(suffix=".dump", delete=False) as tmp:
                for chunk in form.cleaned_data['dump_file'].chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            db_url, env = get_pg_connection()
            cmd = [
                "pg_restore", "--verbose", "--clean", "--no-owner",
                f"--dbname={db_url}", tmp_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, env=env)

            if result.returncode == 0:
                messages.success(request, "Base de datos restaurada correctamente.")
            else:
                messages.error(request, f"Error {result.returncode}: {result.stderr}")

        except Exception as exc:
            messages.error(request, f"Ocurrió un error inesperado: {exc}")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
        return render(request, "restore.html", {"form": form})

    return render(request, 'restore.html', {'form': form})
