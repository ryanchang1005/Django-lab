from system.models import Log


class LogService:

    @staticmethod
    def log_middleware(request):
        try:
            user = request.user if hasattr(request, 'user') else None
            url = request.path if hasattr(request, 'path') else None
            method = request.method if hasattr(request, 'method') else None

            log = Log()
            log.user = user
            log.data = {
                'url': url,
                'method': method,
            }
            log.save()
        except:
            pass
