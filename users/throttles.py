from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        # throttle by IP address
        return self.get_ident(request)


class RegisterThrottle(SimpleRateThrottle):
    scope = "register"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class TokenValidateThrottle(SimpleRateThrottle):
    scope = "token_validate"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
