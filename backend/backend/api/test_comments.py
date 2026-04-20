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
    
    def test_like_then_dislike_removes_like(self):
        self.login()

        self.client.post(f"/api/comments/{self.comment.id}/like/")
        self.client.post(f"/api/comments/{self.comment.id}/dislike/")

        self.comment.refresh_from_db()

        self.assertEqual(self.comment.likes.count(), 0)
        self.assertEqual(self.comment.dislikes.count(), 1)

    def test_dislike_then_like_removes_like(self):
        self.login()
        
        self.client.post(f"/api/comments/{self.comment.id}/dislike/")
        self.client.post(f"/api/comments/{self.comment.id}/like/")

        self.comment.refresh_from_db()

        self.assertEqual(self.comment.dislikes.count(), 0)
        self.assertEqual(self.comment.likes.count(), 1)

    def test_toggle_like_removes_like(self):
        self.login()

        url = f"/api/comments/{self.comment.id}/like/"

        self.client.post(url)
        self.client.post(url)

        self.comment.refresh_from_db()

        self.assertEqual(self.comment.likes.count(), 0)

    #AHAHAHHAAHA! I JUST DUPLICATED TEST BELLOW AND THIS IS TEST WHICH TESTS LIKES DUPLICATE, so ironic innit?
    def test_no_duplication_like(self):
        self.login()

        url = f"/api/comments/{self.comment.id}/like/"

        self.client.post(url)
        self.client.post(url)

        self.comment.refresh_from_db()

        self.assertEqual(self.comment.likes.count(), 0)

    def test_multiple_users_can_like(self):
        self.login()
        self.client.post(f"/api/comments/{self.comment.id}/like/")

        user2 = User.objects.create_user(username="user2", password="123")

        response = self.client.post("/api/token/", {
            "username": "user2",
            "password": "123"
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.client.post(f"/api/comments/{self.comment.id}/like/")

        self.comment.refresh_from_db()

        self.assertEqual(self.comment.likes.count(), 2)

    def test_moderator_can_delete_comment(self):
        moderator = User.objects.create_user(
            username="mod",
            password="123",
            is_staff=True
        )

        response = self.client.post("/api/token/", {
            "username": "mod",
            "password": "123"
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/comments/{self.comment.id}/")

        self.assertIn(response.status_code, [200, 204])
    
    def test_non_author_cannot_delete_comment(self):
        user2 = User.objects.create_user(
            username="user2",
            password="123"
        )

        response = self.client.post("/api/token/", {
            "username": "user2",
            "password": "123"
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/comments/{self.comment.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_author_can_delete_own_comment(self):
        self.login()

        response = self.client.delete(f"/api/comments/{self.comment.id}/")

        self.assertIn(response.status_code, [200, 204])

    def test_invalid_rating_fails(self):
        self.login()

        response = self.client.post("/api/comments/", {
            "discipline": self.discipline.id,
            "text": "Bad rating",
            "rating": 10
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_missing_fields(self):
        self.login()

        response = self.client.post("/api/comments/", {
            "discipline": self.discipline.id
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)