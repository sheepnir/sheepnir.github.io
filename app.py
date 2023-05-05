import os
import openai
from config import api_key
from git import Repo
from pathlib import Path

# Setting up OpenAI API
openai.api_key = api_key

# Setting the folders in the local machine
PATH_TO_BLOG_REPO = Path('/Users/nir-sheep/Developer/sheepnir.github.io/.git')
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/'content'
PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True)




