class TunnelingMiddleware(object):
    def process_request(self, request):
        if request.META.has_key('HTTP_X_METHODOVERRIDE'):
            http_method = request.META['HTTP_X_METHODOVERRIDE']
            if http_method.lower() == 'put':
                request.method = 'PUT'
                request.META['REQUEST_METHOD'] = 'PUT'
            if http_method.lower() == 'delete':
                request.method = 'DELETE'
                request.META['REQUEST_METHOD'] = 'DELETE'
        return None