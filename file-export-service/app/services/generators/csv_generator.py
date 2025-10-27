from io import BytesIO
def generate_csv(report_slug: str):
    buf = BytesIO()
    rows = [["Metric","Value"],["Report",report_slug],["ExampleValue",42]]
    buf.write(("
".join([",".join(map(str,r)) for r in rows]) + "\n").encode("utf-8"))
    buf.seek(0)
    return buf
