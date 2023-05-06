import os
import openai
from config import api_key, LOCAL_PATH
from git import Repo
from pathlib import Path

'''
This is the main file that will be used to run the blog.
It will be used to create the blog and push it to the github repo.
It will also be used to create the blog post.

Packages to install:
    - Git
    - openai
    - GitPython

Create  a config.py file with the following variables:
    - api_key: The API key for OpenAI   
    - LOCAL_PATH: The path to the local repo.
'''


# Setting up OpenAI API
openai.api_key = api_key

# Setting the folders in the local machine
PATH_TO_BLOG_REPO = Path(LOCAL_PATH) 
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent 
PATH_TO_CONTENT = PATH_TO_BLOG/'content'
PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True) #Setting the folder if it doesn't exist

def update_blog(commit_message = 'Updates blog'):
    '''
    This function will update the blog.
    '''
    # GitPython -- Repo location
    repo = Repo(PATH_TO_BLOG_REPO)
    # git add .
    repo.git.add(all=True)
    # git commit -m "Updates blog"
    repo.index.commit(commit_message)
    # git push origin master
    origin = repo.remote(name='origin')
    origin.push()

# Testing the update_blog function
random_text = 'Test Test Test Test'

with open(PATH_TO_BLOG/'index.html', 'w') as f:
    f.write(random_text)

update_blog()
   








