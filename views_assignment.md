# Django Class-Based Views Assignment

## Prerequisites
* Update your fork with the latest commit from the master branch of crcresearch/codecamp-skillinator-django
* Make a branch for the views assignment in your forked repo
* Migrate the database (or delete the old one and start fresh)
* Superuser should be defined in the database already
* Install fixtures (on windows use windows-style slashes in the first one)

    <code>python manage.py loaddata fixtures/auth_initial_data.json</code>
    
    <code>python manage.py loaddata --app skillsmatrix initial_data.json</code>
* At this point, the server should run, but going to any page will throw an error.

## Assignment Details
This assignment is intended to practice writing Class-Based Views in Django. For this exercise, all of the templates and URLs have been written for you. Although they are provided, you must *use them to figure out how to implement your views correctly.* **CHANGES SHOULD ONLY BE MADE TO THE home.py AND developer.py FILES IN THE skillsmatrix/views DIRECTORY!**

IMPORTANT NOTE: the initial data that is loaded in during the 'lodaddata' step of the prerequisites creates 13 users. These user passwords are simply the username repeated 2-3 times, whichever it takes to get to >=8 characters (Django's minimum needed for a password). For example, the user 'jared' has a password of 'jaredjared' but 'nic' has a password of 'nicnicnic'. You will need these to log in as different users to test some of the views as well as to give extra credit without using the admin site.

Here are the views that you need to write to complete the assignment.
* Home - a template view that loads the home.html template file and also puts a few items in the context to display some overall app statistics on the home page.
* DeveloperList - a ListView that lists all of the developers by using the developer_list.html template
* DeveloperListByManager - a ListView that inherits from DeveloperList but uses a url parameter to only show the list of developers that have the manager passed in on the url (Hint: use the skillsmatrix/urls.py file to gain some clues!)
* DeveloperDetail - a DetailView of a single developer, determined by id passed in the urls.py file. This view uses the developer_detail.html template and must load an extra list into the context to get the page to display correctly (Hint: Look at the template file itself to see what the context variable should be called). This extra list should be sorted in **descending order** by years of experience.
* DeveloperDetailMe - a DetailView that inherits from DeveloperDetail, but instead of getting a pk from the URL, always show the detail page of the currently logged in user/developer
* DeveloperUpdate - an UpdateView that uses the developer_update.html template to update a developer's title. After completing the update, this view should redirect back to the developer detail page of the user that was just edited.
* ExtraCreditCreateView - a CreateView that allows the logged in user to send extra credit to another developer. The form does not ask for the sender because it should always be based on the developer of the logged in user. (Extra Credit: Make this view also decrement the extra credit tokens if the extra credit form is valid, and not allowing the user to give extra credit if they don't have any tokens) After successfully creating the extra credit object, this view should return the user back to their own developer detail page.

###### Create a Pull Request of your assignment branch when complete and ready for review.
