from django.core.cache import cache


class RequestLimiter:
    MAX_ATTEMPT_NUMBER: int = 3
    ATTEMPT_REST_TIME: int = 3600

    @staticmethod
    def get_ip_address(request):
        return request.META.get('REMOTE_ADDR')

    @classmethod
    def block_ip_address(cls, ip_address):
        cache.set(f"ip_blocked_{ip_address}",
                  ip_address, cls.ATTEMPT_REST_TIME)
        return True

    @classmethod
    def block_mobile_number(cls, mobile_number):
        cache.set(f"mobile_number_blocked_{mobile_number}",
                  mobile_number, cls.ATTEMPT_REST_TIME)
        return True

    @classmethod
    def check_ip_is_blocked(cls, request):
        ip_address = cls.get_ip_address(request=request)
        return True if cache.get(f"ip_blocked_{ip_address}") else False

    @classmethod
    def attempt(cls, request, request_type, mobile_number: str = None) -> bool:
        if request_type == "register":
            if request:
                ip_address = cls.get_ip_address(request=request)
                cache_value = cache.get(f'attempt_{ip_address}')
                value = cache_value+1 if cache_value else 1
                if value > cls.MAX_ATTEMPT_NUMBER:
                    cls.block_ip_address(ip_address=ip_address)
                else:
                    cache.set(f"attempt_{ip_address}",
                              value, cls.ATTEMPT_REST_TIME)
            if mobile_number:
                cache_value = cache.get(f'attempt_{mobile_number}')
                value = cache_value+1 if cache_value else 1
                if value > cls.MAX_ATTEMPT_NUMBER:
                    cls.block_mobile_number(mobile_number=mobile_number)
                else:
                    cache.set(f"attempt_{mobile_number}",
                              value, cls.ATTEMPT_REST_TIME)
        if request_type == "login":
            if request:
                ip_address = cls.get_ip_address(request=request)
                cache_value = cache.get(f'login_attempt_{ip_address}')
                value = cache_value+1 if cache_value else 1
                if value > cls.MAX_ATTEMPT_NUMBER:
                    cls.block_ip_address(ip_address=ip_address)
                else:
                    cache.set(
                        f"login_attempt_{ip_address}", value, cls.ATTEMPT_REST_TIME)
            if mobile_number:
                cache_value = cache.get(f'login_attempt_{mobile_number}')
                value = cache_value+1 if cache_value else 1
                if value > cls.MAX_ATTEMPT_NUMBER:
                    cls.block_mobile_number(mobile_number=mobile_number)
                else:
                    cache.set(
                        f"login_attempt_{mobile_number}", value, cls.ATTEMPT_REST_TIME)
        return True
