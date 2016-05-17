from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import *
from skillsmatrix.models import *
import json
from bs4 import BeautifulSoup

# FUNCTIONS TO TEST
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

class HomeworkTest(TestCase):
    def setUp(self):
        # Create some users
        user1 = User.objects.create(username='dev1', first_name='Developer', last_name='One')
        user1.set_password('password')
        user1.save()
        dev1 = Developer.objects.create(user=user1, manager='Bill', title='Programmer')
        dev1.save()

        user2 = User.objects.create(username='neo', first_name='Thomas', last_name='Anderson')
        user2.set_password('password')
        user2.save()
        dev2 = Developer.objects.create(user=user2, manager='Bill', title='Programmer')
        dev2.save()

    def test_ProblemOne_POST(self):
        # search for "name"
        factory = RequestFactory()
        request = factory.post('/problem_one_post/', {'name': 'dev1'})
        response = ProblemOne(request)
        self.assertEquals(json.loads(response.content)['name'], 'dev1')

    def test_ProblemOne_POST_None(self):
        # search for "name" is None
        factory = RequestFactory()
        request = factory.post('/problem_one_post/', {})
        response = ProblemOne(request)
        self.assertEquals(json.loads(response.content)['name'], None)

    def test_ProblemOne_developers(self):
        # search for "developers"
        factory = RequestFactory()
        request = factory.get('/problem_one/', {'name': 'Thomas'})
        response = ProblemOne(request)
        self.assertEquals(json.loads(response.content)[0]['first_name'], 'Thomas')

    def test_ProblemTwo_In(self):
        # Create a client for testing with
        client = Client()

        # log in as neo
        client.login(username='neo', password='password')

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'MSIE'})
        self.assertEquals(response.content, "Neo wouldn't use Internet Explorer silly...")

    def test_ProblemTwo_notIn(self):
        # Create a client for testing with
        client = Client()

        # log in as developer1
        client.login(username='neo', password='password')

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'Firefox'})
        self.assertEquals(response['Location'], "http://vignette2.wikia.nocookie.net/matrix/images/d/df/Thematrixincode99.jpg/revision/latest?cb=20140425045724")

    def test_ProblemTwo_notUser(self):
        # Create a client for testing with
        client = Client()

        # log in as developer1
        client.login(username='dev1', password='password')

        response = client.get('/problemtwo/', **{'HTTP_USER_AGENT': 'Firefox'})
        self.assertEquals(response.content, "Operator...")

    def test_ProblemThree(self):
        # create a client for testing with
        client = Client()

        # log in as dev1
        client.login(username='neo', password='password')

        # call the home page URL
        response = client.get('/problemthree/', **{'HTTP_USER_AGENT': 'Firefox'})

        print(str(response))
        self.assertEquals(response.status_code, 200)




