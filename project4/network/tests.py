from django.test import TestCase
from django.db.backends.sqlite3.base import IntegrityError
from django.test import Client
from network.models import *


def login():
    c = Client()
    c.login(username='user1', password='cvbnm,.;/')
    return c

# Create your tests here.

class PostTestCase(TestCase):

    def setUp(self):
        #Create users for test
        u1 = User.objects.create(username="user1", first_name="name1", last_name="last1", email="user1@example.com", password='pbkdf2_sha256$180000$Xv7QDMfHiMl1$06is6iUhEmVbJoTGwnJertRosZTUI2cdPa8W59TOQ2E=')
        u2 = User.objects.create(username="user2", first_name="name2", last_name="last2", email="user2@example.com", password='pbkdf2_sha256$180000$Xv7QDMfHiMl1$06is6iUhEmVbJoTGwnJertRosZTUI2cdPa8W59TOQ2E=')
        u3 = User.objects.create(username="user3", first_name="name3", last_name="last3", email="user3@example.com", password='pbkdf2_sha256$180000$Xv7QDMfHiMl1$06is6iUhEmVbJoTGwnJertRosZTUI2cdPa8W59TOQ2E=')
        u4 = User.objects.create(username="user4", first_name="name4", last_name="last4", email="user4@example.com", password='pbkdf2_sha256$180000$Xv7QDMfHiMl1$06is6iUhEmVbJoTGwnJertRosZTUI2cdPa8W59TOQ2E=')

        #Create Posts
        p1 = Post.objects.create(post_owner_id=1, post_content="Content1")
        p2 = Post.objects.create(post_owner_id=2, post_content="Content2")
        p3 = Post.objects.create(post_owner_id=3, post_content="Content3")  
        p4 = Post.objects.create(post_owner_id=4, post_content="Content4")

        #Create Likes
        l1 = Like.objects.create(like_user_id=1, like_post_id=2)
        l2 = Like.objects.create(like_user_id=2, like_post_id=3)
        l3 = Like.objects.create(like_user_id=3, like_post_id=4)
        l4 = Like.objects.create(like_user_id=4, like_post_id=1)

        #Create Followers
        f1 = Follower.objects.create(user_a_followed_by_b_id=1, user_b_follows_a_id=4)
        f2 = Follower.objects.create(user_a_followed_by_b_id=2, user_b_follows_a_id=1)
        f3 = Follower.objects.create(user_a_followed_by_b_id=3, user_b_follows_a_id=2)
        f4 = Follower.objects.create(user_a_followed_by_b_id=4, user_b_follows_a_id=3)

    
        

    #test create users
    def testUsers(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 4)

    #test create posts
    def testPosts(self):
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 4)

    #test create likes
    def testLikes(self):
        likes = User.objects.all()
        self.assertEqual(likes.count(), 4)

    #test create followers
    def testFollowers(self):
        followers = User.objects.all()
        self.assertEqual(followers.count(), 4)

    #test do not create duplicate followers
    def testNonDuplicatesLikes(self):
        l4 = Like(like_user_id=4, like_post_id=1)
        self.assertRaises(IntegrityError, l4.save)

    #test not to create duplicate followers
    def testNonDuplicatesFollowers(self):
        f4 = Follower(user_a_followed_by_b_id=4, user_b_follows_a_id=3)
        self.assertRaises(IntegrityError, f4.save)

    # #test login page
    def testLoginPage(self):
        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)

    # #test register page
    def testRegisterPage(self):
        c = Client()
        response = c.get('/register')
        self.assertEqual(response.status_code, 200)

    # #test home page
    def testHomePage(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    # test user login
    def testUserLogin(self):
        c = Client()
        response = c.post('/login',{"username":"user1", "password":"cvbnm,.;/"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/feed')

    #test get_user_posts api
    def testGetPosts(self):
        c = login()
        jsonresponse = c.get('/get_posts', follow=True)
        self.assertEqual(jsonresponse.status_code, 200)
        self.assertEqual(jsonresponse['Content-Type'], 'application/json')
        self.assertEqual(len(jsonresponse.json()["post_ids"]), 4)

    # test get_post_info api
    def testGetPostInfo(self):
        c = Client()
        jsonresponse = c.get('/get_post_info', {'post_id': 1}, follow=True)
        self.assertEqual(jsonresponse.status_code, 200)
        self.assertEqual(jsonresponse['Content-Type'], 'application/json')
        self.assertEqual(jsonresponse.json()['post_info'][0]['post_content'], 'Content1')
        self.assertEqual(jsonresponse.json()['post_info'][0]['post_owner_id'], 1)

        





