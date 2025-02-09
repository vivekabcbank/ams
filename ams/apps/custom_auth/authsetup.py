from django.contrib.auth.backends import ModelBackend
from .models import Users

class UserAuthentication(ModelBackend):
	@staticmethod
	def user_authenticate(request=None, **credentials):
		return None
