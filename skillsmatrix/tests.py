from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import *
from skillsmatrix.models import *
import json
from bs4 import BeautifulSoup
import response_tests

# FUNCTIONS TO TEST
from skillsmatrix.views import SearchDeveloperSkill
from homework import ProblemOne, ProblemTwo, ProblemThree

class SkillsMatrix(TestCase):
    def setUp(self):
        # Create some users
        user1 = User.objects.create(username='dev1', first_name='Developer', last_name='One')
        user1.set_password('password')
        user1.save()
        dev1 = Developer.objects.create(user=user1, manager='Bill', title='Programmer')
        dev1.save()

        user2 = User.objects.create(username='dev2', first_name='Developer', last_name='Two')
        user2.set_password('password')
        user2.save()
        dev2 = Developer.objects.create(user=user2, manager='Bill', title='Programmer')
        dev2.save()

        # Create a skill
        skill1 = Skill.objects.create(name='Angular', family='Front-End', difficulty=1)
        skill1.save()

        skill2 = Skill.objects.create(name='C++', family='Back-End', difficulty=2)
        skill2.save()

        skill3 = Skill.objects.create(name='PhotoShop', family='Front-End', difficulty=0)
        skill3.save()

        # Add skill sets to users
        # dev1 gets skills 1 and 3
        skillset_dev1_skill1 = DeveloperSkill.objects.create(developer=dev1, skill=skill1, proficiency='Eh',
                                                             years_of_experience=2)
        skillset_dev1_skill1.save()

        skillset_dev1_skill3 = DeveloperSkill.objects.create(developer=dev1, skill=skill3, proficiency='Good',
                                                             years_of_experience=8)
        skillset_dev1_skill3.save()

        # dev2 gets skills 2 and 3
        skillset_dev2_skill2 = DeveloperSkill.objects.create(developer=dev2, skill=skill2,
                                                             proficiency='Enough to cause trouble',
                                                             years_of_experience=6)
        skillset_dev2_skill2.save()

        skillset_dev2_skill3 = DeveloperSkill.objects.create(developer=dev2, skill=skill3,
                                                             proficiency='I can art.',
                                                             years_of_experience=20)
        skillset_dev2_skill3.save()

    def test_DeveloperSkillSearch(self):
        # search for "Angular" (should have 1 result)
        factory = RequestFactory()
        request = factory.get('/search_developer_skillset/', {'skill': 'Angular'})
        response = SearchDeveloperSkill(request)
        self.assertEquals(len(json.loads(response.content)), 1)
        self.assertEquals(json.loads(response.content)[0]['developer__user__username'], 'dev1')

        # search for "C++" (should have 1 result)
        factory = RequestFactory()
        request = factory.get('/search_developer_skillset/', {'skill': 'C++'})
        response = SearchDeveloperSkill(request)
        self.assertEquals(len(json.loads(response.content)), 1)
        self.assertEquals(json.loads(response.content)[0]['developer__user__username'], 'dev2')

        # search for "Photoshop" (should have 2 results)
        factory = RequestFactory()
        request = factory.get('/search_developer_skillset/', {'skill': 'Photoshop'})
        response = SearchDeveloperSkill(request)
        self.assertEquals(len(json.loads(response.content)), 2)
        self.assertEquals(json.loads(response.content)[0]['developer__user__username'], 'dev1')
        self.assertEquals(json.loads(response.content)[1]['developer__user__username'], 'dev2')

        # search for "Cooking" (should not exist)
        factory = RequestFactory()
        request = factory.get('/search_developer_skillset/', {'skill': 'Cooking'})
        response = SearchDeveloperSkill(request)
        self.assertEquals(len(json.loads(response.content)), 0)

        # Fail to put in a skill
        factory = RequestFactory()
        request = factory.get('/search_developer_skillset/', {})
        response = SearchDeveloperSkill(request)
        self.assertEquals(('ERROR' in json.loads(response.content)), True)
        self.assertEquals(json.loads(response.content)['ERROR'], 'No skillset listed!')

    def test_MySkillsDev1(self):
        # Create a client for testing with
        client = Client()

        # log in as developer1
        client.login(username='dev1', password='password')

        response = client.get('/myskills/')
        skills1 = json.loads(response.content)
        self.assertEquals(len(skills1), 2)
        self.assertEquals(str(skills1[0]), 'Angular')
        self.assertEquals(str(skills1[1]), 'PhotoShop')

        # now log in as dev 2 and check their skills
        client.login(username='dev2', password='password')

        response = client.get('/myskills/')
        skills2 = json.loads(response.content)
        self.assertEquals(len(skills2), 2)
        self.assertEquals(str(skills2[0]), 'C++')
        self.assertEquals(str(skills2[1]), 'PhotoShop')

    def test_HomePage(self):
        # create a client for testing with
        client = Client()

        # log in as dev1
        client.login(username='dev1', password='password')

        # call the home page URL
        response = client.get('/homepage/', **{'HTTP_USER_AGENT': 'Firefox'})
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(('dev1' in soup.find('h2', {'id': 'username'})), True)

        # check again, using IE
        response = client.get('/homepage/', **{'HTTP_USER_AGENT': 'MSIE'})
        self.assertEquals('IE not supported', response.content)

class HomeworkClass(TestCase):
    def setUp(self):
        # Create some users
        user1 = User.objects.create(username='neo', first_name='Keanu', last_name='Reeves')
        user1.set_password('matrix')
        user1.save()
        dev1 = Developer.objects.create(user=user1, manager='Morpheus', title='Programmer')
        dev1.save()

        user2 = User.objects.create(username='beth', first_name='Beth', last_name='Caldwell')
        user2.set_password('bethbeth')
        user2.save()
        dev2 = Developer.objects.create(user=user2, manager='Dave', title='Programmer')
        dev2.save()

        user3 = User.objects.create(username='jared', first_name='Jared', last_name='Olson')
        user3.set_password('sweden')
        user3.save()
        dev3 = Developer.objects.create(user=user3, manager='Caleb', title='Associate Programmer')
        dev3.save()

        user4 = User.objects.create(username='trinity', first_name='', last_name='')
        user4.set_password('trinity')
        user4.save()
        dev4 = Developer.objects.create(user=user4, manager='Morpheus', title='Programmer')
        dev4.save()

        self.factory = RequestFactory()

    def test_Problem1_postName(self):
        request = self.factory.post('/problem-one/', {'name': 'Beth'})
        response = ProblemOne(request)
        print "RESPONSE: ", response.content
        self.assertEqual(json.loads(response.content)["name"], "Beth")

    def test_Problem1_postNoName(self):
        request = self.factory.post('/problem-one/', {'location': 'The Matrix'})
        response = ProblemOne(request)
        print "RESPONSE: ", response.content
        self.assertEqual(json.loads(response.content)['name'], None)

    def test_Problem1_get(self):
        request = self.factory.get('/problem-one/', {'name': 'Beth'})
        response = ProblemOne(request)
        print "RESPONSE: ", response.content
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Beth')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Caldwell')
        self.assertEqual(json.loads(response.content)[0]['location'], 'CRC')

    def test_Problem1_getNeo(self):
        request = self.factory.get('/problem-one/', {'name': 'Keanu'})
        response = ProblemOne(request)
        print "RESPONSE: ", response.content
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Keanu')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Reeves')
        self.assertEqual(json.loads(response.content)[0]['location'], 'The Matrix')

    def test_Problem2_IE(self):
        client = Client()

        client.login(username='neo', password='matrix')

        # call the home page URL

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'MSIE'})
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual("Neo wouldn't use Internet Explorer silly...", response.content)

    def test_Problem2_Firefox(self):
        client = Client()

        client.login(username='neo', password='matrix')

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'Firefox'})
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 302)

    def test_Problem2_diffUserIE(self):
        client = Client()

        client.login(username='beth', password='bethbeth')

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'MSIE'})
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual("Operator...", response.content)

    def test_Problem2_diffUserFirefox(self):
        client = Client()

        client.login(username='beth', password='bethbeth')

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'Firefox'})
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual("Operator...", response.content)

    def test_Problem3Name(self):
        client = Client()

        client.login(username='beth', password='bethbeth')

        response = client.get('/problemthree/', **{'HTTP_USER_AGENT': 'Firefox'})
        print "RESPONSE: ", response
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Beth Caldwell' in str(soup.find('span', {'id': 'name'})), True)

    def test_Problem3UserName(self):
        client = Client()

        client.login(username='trinity', password='trinity')

        response = client.get('/problemthree/', **{'HTTP_USER_AGENT': 'Firefox'})
        print "RESPONSE: ", response
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('trinity' in str(soup.find('span', {'id': 'name'})), True)



