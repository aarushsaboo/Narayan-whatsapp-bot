
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(transactions):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica", 14)
    p.drawString(100, height - 50, "Transaction Receipt Summary")

    p.setFont("Helvetica", 10)
    y = height - 100
    for txn in transactions:
        line = (
            f"ID: {txn['transaction_id']}, ₹{txn['amount']}, "
            f"{txn['transaction_date'].strftime('%Y-%m-%d')}, "
            f"{txn['payment_method']} ({txn['status']})"
        )
        p.drawString(50, y, line)
        y -= 20
        if y < 50:  # new page if overflow
            p.showPage()
            y = height - 50

    p.save()
    buffer.seek(0)
    return buffer.read()

