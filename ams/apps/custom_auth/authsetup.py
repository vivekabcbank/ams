from django.contrib.auth.backends import ModelBackend
from .models import Users

class UserAuthentication(ModelBackend):
	@staticmethod
	def user_authenticate(request=None, **credentials):
		return None

class MiddlewarePrintRequest:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		try:
			print(f"Request method: {request.method}")
			print(f"Request path: {request.path}")

			print("Request headers:")
			for header, value in request.headers.items():
				print(f"{header}: {value}")

			if request.method == "POST":
				print("Request body:")
				print(request.body.decode('utf-8'))

			response = self.get_response(request)

			response['X-Custom-Header'] = 'This is a custom header'
		except Exception as e:
			print(e)
		response = self.get_response(request)
		return response