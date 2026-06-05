from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstUserRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'

class BurstAnonRateThrottle(AnonRateThrottle):
    scope = 'burst'

class SustainedAnonRateThrottle(AnonRateThrottle):
    scope = 'sustained'

