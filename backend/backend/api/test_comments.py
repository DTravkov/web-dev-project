from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Discipline, Comment


class CommentAPITest(APITestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "password123"

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        self.discipline = Discipline.objects.create(
            name="Test Discipline",
            approved_by=self.user
        )

        self.comment = Comment.objects.create(
            author=self.user,
            discipline=self.discipline,
            content="Test comment",
            rating=5
        )
    def login(self):
        response = self.client.post("/api/token/", {
            "username": self.username,
            "password": self.password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_comment_authorized(self):
        self.login()

        response = self.client.post("/api/comments/", {
            "discipline": self.discipline.id,
            "content": "Nice discipline",  
            "rating": 5
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_comment_unauthorized(self):
        response = self.client.post("/api/comments/", {
            "discipline": self.discipline.id,
            "content": "Nice discipline", 
            "rating": 5
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_like_comment(self):
        self.login()
        response = self.client.post(f"/api/comments/{self.comment.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_dislike_comment(self):
        self.login()

        response = self.client.post(f"/api/comments/{self.comment.id}/dislike/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_toggle_like_comment(self):
        self.login()

        url = f"/api/comments/{self.comment.id}/like/"

        response1 = self.client.post(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT) 

        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT) 

    def test_like_comment_unauthorized(self):
        response = self.client.post(f"/api/comments/{self.comment.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)