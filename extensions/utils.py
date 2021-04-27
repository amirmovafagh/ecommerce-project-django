from decouple import config
from django.utils import timezone
from kavenegar import *

from extensions import jalali


def jalali_converter(datetime):
    jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذز", "دی", "بهمن", "اسفند", ]

    datetime = timezone.localtime(datetime)  # change time to target timezone in settings.py

    time_to_str = "{},{},{}".format(datetime.year, datetime.month, datetime.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = "{} {} {}، ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        datetime.hour,
        datetime.minute,
    )
    return output


def send_message_api(phone, message):
    try:
        api = KavenegarAPI(config('KAVENEGAR_API'))
        params = {
            'sender': '1000596446',  # optional
            'receptor': phone,  # multiple mobile number, split by comma
            'message': message,
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
