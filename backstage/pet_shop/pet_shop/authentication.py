"""
Custom authentication helpers for the project.
"""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
	"""
	Disable CSRF enforcement for DRF endpoints that rely on session cookies.

	This keeps the convenience of SessionAuthentication (so existing login
	flow continues工作) while preventing 403 errors when the frontend does
	not send CSRF tokens for AJAX calls.
	"""

	def enforce_csrf(self, request):
		return
