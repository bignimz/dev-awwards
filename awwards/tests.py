from django.test import TestCase
from .models import Project,User, Profile


# Create your tests here.

class ProfileTest(TestCase):
    '''
    test class for Profile model
    '''
    def setUp(self):
        '''
        test method to create Profile instances called before all tests
        '''
        self.new_user = User(username='hulla')
        self.new_user.save()
        self.new_profile = Profile(name='balloo',pic='images/picture.jpeg',bio='web designer',user=self.new_user,location='nairobi',contact='hullaballoo@gamil.com')
        self.new_profile.save()


    def tearDown(self):
        '''
        test method to delete Profile instances after each test is run
        '''
        Profile.objects.all().delete()


    def test_save_profile(self):
        '''
        test method to ensure a Profile instance has been correctly saved
        '''
        self.assertTrue(len(Profile.objects.all()) == 1)


    def test_delete_profile(self):
        '''
        test method to ensure a Profile instance has been correctly deleted
        '''
        self.new_profile.save()
        self.new_profile.delete()
        self.assertTrue(len(Profile.objects.all()) == 0)



class ProjectTest(TestCase):
    '''
    test class for Project model
    '''
    def setUp(self):
        '''
        Function method to create project instances called before all tests
        '''
        self.new_user = User(username='')
        self.new_user.save()
        self.new_project = Project(project_image='images/picture.jpeg', project_name='project one', project_description='this is a project description', user=self.new_user)
        self.new_project.save()
        self.another_project = Project(project_image='images/photo.jpg', project_name='project two', project_description='this is a project description', user=self.new_user)
        self.another_project.save()

    def tearDown(self):
        '''
        test method to delete Project instances after each test is run
        '''
        Project.objects.all().delete()

    def test_save_project(self):
        '''
        test method to ensure an Project instance has been correctly saved
        '''
        self.assertTrue(len(Project.objects.all()) == 2)

    def test_instances(self):
        '''
        test method to assert instances created during setUp
        '''
        self.assertTrue(isinstance(self.new_project,Project))

    def test_delete_project(self):
        '''
        test method to ensure an Image instance has been correctly deleted
        '''
        self.new_project.delete()
        self.assertTrue(len(Project.objects.all()) == 1)
