import os
from datetime import datetime
from celery import shared_task
from app.services.export_registry import export_handlers
EXPORT_DIR = os.getenv("EXPORT_DIR", "/tmp/exports")
os.makedirs(EXPORT_DIR, exist_ok=True)
@shared_task(bind=True)
def generate_export_task(self, report_slug: str, fmt: str):
    handler = export_handlers.get(fmt)
    if not handler:
        raise ValueError(f"Unsupported format: {fmt}")
    data = handler(report_slug)
    filename = f"{report_slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{fmt}"
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "wb") as f:
        f.write(data.getbuffer())
    return {"filename": filename, "path": path}
