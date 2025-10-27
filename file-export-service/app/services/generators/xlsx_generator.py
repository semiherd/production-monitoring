from io import BytesIO
import pandas as pd
def generate_xlsx(report_slug: str):
    buf = BytesIO()
    df = pd.DataFrame([{"Metric":"Report","Value":report_slug},{"Metric":"ExampleValue","Value":42}])
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
    buf.seek(0)
    return buf
