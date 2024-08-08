from base.celery import app
from django.core.cache import cache


@app.task
def send_verification_code(mobile_number, verify_code):
    """kavenegar api for sending sms"""
    # api = KavenegarAPI('')
    # params = {'receptor': mobile,
    #           'token': '%d' % verify_code,
    #           'type': 'sms', 'template': 'verify'}
    cache.set(f'registration_code_{mobile_number}', verify_code, timeout=300)
    
    # api.verify_lookup(params)
