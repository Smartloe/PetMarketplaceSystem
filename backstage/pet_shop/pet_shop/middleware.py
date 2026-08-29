"""
Custom middleware to restore clickjacking protection that SimpleUI removes.

SimpleUI's AppConfig.ready() unconditionally pops XFrameOptionsMiddleware from
MIDDLEWARE because its admin UI relies on iframes.  This middleware re-adds the
header for every non-admin path so the rest of the site stays protected.
"""

from django.conf import settings


class SecurityHeadersMiddleware:
    """
    Add security headers that SimpleUI strips from the default middleware stack.

    Currently handles:
    - X-Frame-Options (clickjacking protection) for non-admin paths
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only add X-Frame-Options to non-admin paths.
        # SimpleUI needs iframes for its admin UI, so /admin/ paths must stay
        # unprotected (or use ALLOWED_FRAME_ORIGINS in Django 4.2+).
        if not request.path.startswith('/admin/'):
            # Use the same value that would come from XFrameOptionsMiddleware
            # when X_FRAME_OPTIONS is set to 'DENY' (the secure default).
            x_frame_options = getattr(settings, 'X_FRAME_OPTIONS', 'DENY').upper()
            if x_frame_options in ('DENY', 'SAMEORIGIN'):
                response['X-Frame-Options'] = x_frame_options

        return response