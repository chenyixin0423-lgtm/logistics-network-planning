"""Public interface for the team's excluded route-planning implementation."""


def getRoutePlanService(inputfile, use_cache_flag, time_limit,
                        strategy='时间最短', pickup_delivery='取货',
                        obj='cost', max_residence_time=99999):
    """Keep the API contract without distributing another member's solver."""
    return {
        'status': 'unavailable',
        'message': 'The team route-planning algorithm is not distributed in this portfolio.'
    }
