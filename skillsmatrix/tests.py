import json

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, Client
from bs4 import BeautifulSoup

from skillsmatrix.models import *
from skillsmatrix.views import SearchDeveloperSkill
from homework import ProblemOne


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
        soup = BeautifulSoup(response.content, 'html')
        self.assertEquals(('dev1' in soup.find('h2', {'id': 'username'})), True)

        # check again, using IE
        response = client.get('/homepage/', **{'HTTP_USER_AGENT': 'MSIE'})
        self.assertEquals('IE not supported', response.content)


class Homework(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user1 = User.objects.create(username='neo', first_name='Thomas', last_name='Anderson')
        user1.set_password('password')
        user1.save()
        dev1 = Developer.objects.create(user=user1, manager='Morpheus', title='Captain of the Nebuchadnezzar')
        dev1.save()

        self.factory = RequestFactory()
        user2 = User.objects.create(username='trinity', first_name='Not', last_name='Known')
        user2.set_password('password')
        user2.save()
        dev2 = Developer.objects.create(user=user2, manager='Morpheus', title='Captain of the Nebuchadnezzar')
        dev2.save()

        self.client = Client()
        self.client.login(username='neo', password='password')

    def test_problem_one_post_name(self):
        request = self.factory.post('/test/', {'name': 'neo'})
        response = ProblemOne(request)
        self.assertEqual(json.loads(response.content)['name'], 'neo')

    def test_problem_one_post_no_name(self):
        request = self.factory.post('/test/', {})
        response = ProblemOne(request)
        self.assertEqual(json.loads(response.content)['name'], None)

    def test_problem_one_get_success(self):
        request = self.factory.get('/test/', {'name': 'Thomas'})
        response = ProblemOne(request)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Thomas')

    def test_problem_two_MSIE(self):
        response = self.client.get(reverse('problem_two'), **{'HTTP_USER_AGENT': 'MSIE'})
        self.assertEqual(response.content, "Neo wouldn't use Internet Explorer silly...")

    def test_problem_two_not_MSIE(self):
        response = self.client.get(reverse('problem_two'), **{'HTTP_USER_AGENT': 'Firefox'})
        print "Response: ", response.content
        print "Code? ", response.status_code
        self.assertEqual(response.status_code, 302)

    def test_problem_two_not_neo(self):
        self.client.login(username='trinity', password='password')
        response = self.client.get(reverse('problem_two'), **{'HTTP_USER_AGENT': 'Firefox'})
        self.assertEqual(response.content, "Operator...")

    def test_problem_three(self):
        self.client.login(username='neo', password='password')
        response = self.client.get(reverse('problem_three'))
        soup = BeautifulSoup(response.content, 'html')
        self.assertEqual(('Thomas Anderson' in str(soup.find('span', {'id': 'name'}))), True)
