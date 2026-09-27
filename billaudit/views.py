from django.shortcuts import render

# Create your views here.
from .ocr_utils import extract_text_from_image, parse_line_items, check_bill

def upload_bill(request):
    if request.method == 'POST' and request.FILES.get('bill_image'):
        bill = Bill(user=request.user, bill_image=request.FILES['bill_image'])
        bill.save()  # save first so bill.bill_image.path exists

        raw_text = extract_text_from_image(bill.bill_image.path)
        items = parse_line_items(raw_text)
        findings = check_bill(items, stated_total=bill.total_amount)

        bill.extracted_text = raw_text
        bill.analysis_result = str(findings)  # for MVP; ideally use a JSONField
        bill.save()

        return render(request, 'billaudit/bill_result.html', {'bill': bill, 'findings': findings})
    return render(request, 'billaudit/upload_bill.html')