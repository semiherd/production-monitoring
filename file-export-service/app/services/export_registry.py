from typing import Callable, Dict
from app.services.generators import pdf_generator, csv_generator, xlsx_generator
export_handlers: Dict[str, Callable[[str], "BytesIO"]] = {}
def register_export(fmt: str):
    def decorator(func):
        export_handlers[fmt] = func
        return func
    return decorator
@register_export("pdf")
def pdf_handler(report_slug: str): return pdf_generator.generate_pdf(report_slug)
@register_export("csv")
def csv_handler(report_slug: str): return csv_generator.generate_csv(report_slug)
@register_export("xlsx")
def xlsx_handler(report_slug: str): return xlsx_generator.generate_xlsx(report_slug)
