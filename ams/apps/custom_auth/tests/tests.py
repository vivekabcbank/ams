from django.test import TestCase
# Write sample test case for TestCase for understanding purpose

from django.urls import reverse
from rest_framework.test import APITestCase
from ..allfunctions import decode_str, encode_str
from ..models import *
import coverage
import json
from pdb import set_trace


# python manage.py test ams.apps.custom_auth
# coverage run manage.py test ams.apps.custom_auth
# coverage html

class TestWebApi(APITestCase):

    def test_AMSApi(self):
        cov = coverage.Coverage()
        cov.start()

        self.userauth = None
        self.admin_usertype_id = None
        self.supervisor_usertype_id = None
        self.employee_usertype_id = None
        self.token = None
        self.site_info_id = None

        try:
            self.database_setup()
            self.userSignup_blank_submit()
            self.userSignup_invalid_email()

            self.signup_user()
            self.signin_user()
            self.insert_employee()

        finally:
            cov.stop()
            cov.save()
            cov.html_report(directory="coverage_report")

    def database_setup(self):
        user = Users.objects.create(
            company_name="google pvt ltd",
            first_name="admin",
            last_name="athilkar",
            email="admin@gmail.com",
            gender="M",
            dob="1991-12-11",
            callingcode="91",
            phone="9665200471",
            address="NDIRA NAGAR TUMSAR BHANDARA MAHARASHTRA ",
            pincode="441912",
            country="India",
            state="Maharashtra",
            city="Nagpur",
            password="asdf1234",
            is_superuser=True
        )
        self.userauth = encode_str(user.id)
        authtoken = Token.objects.get(user=user)
        self.token = authtoken.key

        admin_user_type = UserType.objects.create(typename="Admin")
        supervisor_user_type = UserType.objects.create(typename="Supervisor")
        employee_user_type = UserType.objects.create(typename="Employee")
        self.admin_usertype_id = encode_str(admin_user_type.id)
        self.supervisor_usertype_id = encode_str(supervisor_user_type.id)
        self.employee_usertype_id = encode_str(employee_user_type.id)

        site_info = Site.objects.create(
            address="Lorem ipsum is a dummy or placeholder text commonly used in graphic design, publishing.",
            country="India",
            state="Maharastra",
            city="Nagpur",
            latitude="12.34",
            longitude="13.45",
            sitename="IMG",
            owner_user_id=user.id
        )
        self.site_info_id = encode_str(site_info.id)

    def userSignup_blank_submit(self):
        print("")
        print("")
        print("-----------------------------UserSignup_blank_submit")
        print("")
        url = reverse('signup-user')
        data = {"first_name": '',
                "last_name": '',
                "email": '',
                "username": '',
                "usertype_id": '',
                'gender': '',
                "dob": '',
                'callingcode': "",
                "phone": "",
                "address": "",
                "pincode": "",
                "country": "",
                "state": "",
                "city": "",
                "company_name": "",
                "password": ""
                }

        response = self.client.post(url, data, format='json')
        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 204)

    def userSignup_invalid_email(self):
        print("")
        print("")
        print("-----------------------------UserSignup_invalid_email")
        print("")
        url = reverse('signup-user')
        data = {
            "company_name": "google pvt ltd",
            "first_name": "vivek",
            "last_name": "athilkar",
            "email": "vivek2gmail.com",
            "gender": "M",
            "dob": "1991-12-11",
            "callingcode": "91",
            "phone": "9665200490",
            "address": "NDIRA NAGAR TUMSAR BHANDARA MAHARASHTRA ",
            "pincode": "441912",
            "usertype_id": self.admin_usertype_id,
            "country": "India",
            "state": "Maharashtra",
            "city": "Nagpur",
            "password": "asdf1234"
        }

        response = self.client.post(url, data, format='json')
        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")

        self.assertEqual(status, 204)

    def signup_user(self):
        print("")
        print("")
        print("-----------------------------UserSignup")
        print("")
        url = reverse('signup-user')
        data = {
            "company_name": "google pvt ltd",
            "first_name": "vivek",
            "last_name": "athilkar",
            "email": "vivek@gmail.com",
            "gender": "M",
            "dob": "1991-12-11",
            "callingcode": "91",
            "phone": "9665200472",
            "address": "NDIRA NAGAR TUMSAR BHANDARA MAHARASHTRA ",
            "pincode": "441912",
            "usertype_id": self.employee_usertype_id,
            "country": "India",
            "state": "Maharashtra",
            "city": "Nagpur",
            "password": "asdf1234"
        }

        response = self.client.post(url, data, format='json')

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def signin_user(self):
        print("")
        print("")
        print("-----------------------------UserSignin")
        print("")
        url = reverse('signin-user')
        data = {
            "username": "919665200472",
            "password": "asdf1234",
        }

        response = self.client.post(url, data, format='json')

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def insert_employee(self):
        print("")
        print("")
        print("-----------------------------Insert Employee")
        print("")
        url = reverse('insert-employee')
        data = {
            "company_name": "google pvt ltd",
            "first_name": "Avaneesh",
            "last_name": "Athilkar",
            "usertype_id": self.employee_usertype_id,
            "gender": "M",
            "callingcode": "91",
            "phone": "9665200452",
            "address": "Lorem ipsum is a dummy or placeholder text commonly used in graphic design.",
            "pincode": "441912",
            "country": "India",
            "state": "Maharashtra",
            "city": "Nagpur",
            "site_info_id": self.site_info_id,
            "qualification": "BSC",
            "joiningdate": "1991-12-11",
            "min_wages": 333
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)