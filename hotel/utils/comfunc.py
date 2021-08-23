from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from hotel.utils import constants

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
