import unittest
import requests


class APITestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Replace with your API base URL
    access_token = None


    def test_01_register_user(self):
        url = self.BASE_URL + "/register"
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass"
        }
        response = requests.post(url, json=data)
        self.assertIn("message", response.json())
        self.assertEqual(response.status_code, 201)

    def test_02_login(self):
        url = self.BASE_URL + "/login"
        data = {
            "username": "testuser",
            "password": "testpass"
        }
        response = requests.post(url, json=data)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.status_code, 200)
        self.__class__.access_token = response.json()["access_token"]  # Store the access token

    def test_03_add_project(self):
        url = self.BASE_URL + "/project/add"
        data = {
            "title": "New Project",
            "description": "Project description"
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("project", response.json())

    def test_04_get_all_projects(self):
        url = self.BASE_URL + "/projects"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("projects", response.json())

    def test_05_get_project_by_id(self):
        project_id = 1  # Replace with a valid project ID
        url = self.BASE_URL + f"/project/{project_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        self.assertIn(response.status_code, [200, 404])

    def test_06_add_task_to_project(self):
        project_id = 1  # Replace with a valid project ID
        url = self.BASE_URL + f"/project/{project_id}/task/add"
        data = {
            "title": "New Task",
            "description": "Task description",
            "priority": 1,
            "assignee_id": 1  # Replace with a valid assignee ID
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("task", response.json())

    def test_07_update_task_in_project(self):
        project_id = 1  # Replace with a valid project ID
        task_id = 1  # Replace with a valid task ID
        url = self.BASE_URL + f"/project/{project_id}/task/{task_id}"
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "priority": 2,
            "assignee_id": 1  # Replace with a valid assignee ID
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.put(url, json=data, headers=headers)
        self.assertIn(response.status_code, [200, 403, 404])

    def test_08_delete_task_from_project(self):
        project_id = 1  # Replace with a valid project ID
        task_id = 1  # Replace with a valid task ID
        url = self.BASE_URL + f"/project/{project_id}/task/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.delete(url, headers=headers)
        self.assertIn(response.status_code, [200, 403, 404])

    def test_09_delete_project(self):
        project_id = 1  # Replace with a valid project ID
        url = self.BASE_URL + f"/project/delete/{project_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.delete(url, headers=headers)
        self.assertIn(response.status_code, [200, 403, 404])


if __name__ == '__main__':
    unittest.main()
