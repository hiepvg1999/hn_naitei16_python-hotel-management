from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from hotel.utils import constants
import matplotlib.pyplot as plt
import io, base64

def validate_date(request, start, end, bookStart, bookEnd):
    now = datetime.now()
    bookStart = datetime.strptime(bookStart, constants.DATE_FORMAT)
    bookEnd = datetime.strptime(bookEnd, constants.DATE_FORMAT)
    if now > bookStart or now > bookEnd:
        messages.error(request, _("Start date and End date >= now"))
        return False
    else:
        if bookStart > bookEnd:
            messages.error(request, _("End date >= Start date"))
            return False
        else:
            if start <= bookStart.date() <= end:
                messages.error(request, _("Start date has been booked"))
                return False
            elif start <= bookStart.date() <= end:
                messages.error(request, _("End date has been booked"))
                return False
            elif bookStart.date() < start and end < bookEnd.date():
                messages.error(request, _("The date has been booked"))
                return False
            else:
                return True

def get_total_all_bill(bills):
    total = 0
    for bill in bills:
        if int(bill.booking_id.reservation_date.strftime("%m")) == datetime.now().month and bill.booking_id.status == constants.APPROVED:
            total += bill.totalAmount
    return total

def build_chart(keys, values, color= "maroon", width= 0.4, xlabel= _("Booking types"),\
                         ylabel= _("Num of booking for each types"), title= _("Booking figure")):
    fig = plt.figure(figsize = (10, 5))
    plt.bar(keys, values, color= color, width = width)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64
