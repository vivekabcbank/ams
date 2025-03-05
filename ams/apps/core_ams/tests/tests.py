from django.test import TestCase
# Write sample test case for TestCase for understanding purpose

from django.urls import reverse
from rest_framework.test import APITestCase
from ...custom_auth.allfunctions import decode_str, encode_str
from ...custom_auth.models import *
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
        self.employee_id = None

        try:
            self.database_setup()

            self.insert_admin_user_type()
            self.insert_supervisor_user_type()
            self.insert_employee_user_type()

            self.insert_site()
            self.insert_employee()
            self.get_usertypes()
            self.get_sites()
            self.get_employee()
            self.apply_leave()
            self.make_superviser()
            self.mark_attendance()

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

    def insert_admin_user_type(self):
        print("")
        print("")
        print("-----------------------------Insert user type")
        print("")
        url = reverse('insert-user-type')
        data = {
            "userauth": self.userauth,
            "typename": "Admin"
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        self.admin_usertype_id = get_response["result"]["id"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def insert_supervisor_user_type(self):
        print("")
        print("")
        print("-----------------------------Insert user type")
        print("")
        url = reverse('insert-user-type')
        data = {
            "userauth": self.userauth,
            "typename": "Supervisor"
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        self.admin_usertype_id = get_response["result"]["id"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)


    def insert_employee_user_type(self):
        print("")
        print("")
        print("-----------------------------Insert user type")
        print("")
        url = reverse('insert-user-type')
        data = {
            "userauth": self.userauth,
            "typename": "Employee"
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        self.employee_usertype_id = get_response["result"]["id"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)


    def insert_site(self):
        print("")
        print("")
        print("-----------------------------Insert site")
        print("")
        url = reverse('insert-site')
        data = {
            "address": "Lorem ipsum is a dummy or placeholder text commonly used in graphic design, publishing.",
            "country": "India",
            "state": "Maharastra",
            "city": "Nagpur",
            "latitude": "12.34",
            "longitude": "13.45",
            "sitename": "IMG",
            "owner_user_id": self.userauth
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        self.site_info_id = get_response["result"]["id"]
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
        self.employee_id = get_response["employee_id"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def get_usertypes(self):
        print("")
        print("")
        print("-----------------------------Get usertypes")
        print("")
        url = reverse('get-usertypes')

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def get_sites(self):
        print("")
        print("")
        print("-----------------------------Get sites")
        print("")
        url = reverse('get-sites')

        data = {
            "owner_user_id": self.userauth,
            "usertype_id": self.admin_usertype_id
        }

        response = self.client.get(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def get_employee(self):
        print("")
        print("")
        print("-----------------------------Get employee")
        print("")
        url = reverse('get-employee')

        data = {
            "site_info_id": self.site_info_id,
        }

        response = self.client.get(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def apply_leave(self):
        print("")
        print("")
        print("-----------------------------Apply leave")
        print("")
        url = reverse('apply-leave')

        data = {
            "site_info_id": self.site_info_id,
            "employee_id": self.employee_id,
            "start_date": "2025-02-11",
            "end_date": "2025-02-15",
            "reason": "Lorem ipsum is a dummy or placeholder text commonly used in graphic design, publishing"
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def make_superviser(self):
        print("")
        print("")
        print("-----------------------------Make superviser")
        print("")
        url = reverse('make-superviser')

        data = {
            "employee_id": self.employee_id,
            "password": "asdf1234"
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)

    def mark_attendance(self):
        print("")
        print("")
        print("-----------------------------mark-attendance")
        print("")
        url = reverse('mark-attendance')

        attendance_data = json.dumps([
            {"employee_id": self.employee_id,
             "site_info_id": self.site_info_id,
             "attendance": "HD",
             "date": "2025-02-15"},
        ])

        data = {
            "attendance_data": attendance_data
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))

        get_response = json.loads(response.content.decode('utf8'))

        print("\nResult:\n")
        print(get_response)

        print(f"\nStatus Code: {response.status_code}")
        status = get_response["status"]
        print(f"\nStatus Code from end point: {status}")
        self.assertEqual(status, 200)
