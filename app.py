import os
import openai
from config import api_key, LOCAL_PATH
from git import Repo
from pathlib import Path
import shutil
from bs4 import BeautifulSoup as Soup



'''
This is the main file that will be used to run the blog.
It will be used to create the blog and push it to the github repo.
It will also be used to create the blog post.

Packages to install:
    - Git
    - openai
    - GitPython
    - beautifulsoup4

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

'''
# Testing the update_blog function by updating the index.html file and pushing to github
random_text = 'Hello World!!'

with open(PATH_TO_BLOG/'index.html', 'w') as f:
    f.write(random_text)

update_blog()
'''

'''
Function to create a new blog post
It gets a title
content from GPT
cover_image from Dall-E

It creates an HTML file with the title, content and cover_image
'''

def create_blog_post(title, content, cover_image):
    cover_image = Path(cover_image)

    files = len(list(PATH_TO_CONTENT.glob('*.html'))) # Counting all the html files in the content folder
    new_title = f'{files+1}.html' # Creating a new title for the new blog post
    path_to_new_content = PATH_TO_CONTENT/new_title # Creating the path to the new title

    shutil.copy(cover_image, PATH_TO_CONTENT) # Copying the cover image to the new content

    if not os.path.exists(path_to_new_content): 
        # Creating the new content file if it doesn't exist
        with open(path_to_new_content, 'w') as f:
            f.write('<! DOCTYPE html>\n')
            f.write(f'<html>\n')
            f.write(f'<head>\n')
            f.write(f'<title>{title}</title>\n')
            f.write(f'</head>\n')
            f.write(f'<body>\n')
            f.write(f'<img src="{cover_image.name}" alt="Cover Image"><br/>\n')
            f.write(f'<h1>{title}</h1>\n')
            f.write(f'<p>{content}</p>\n')
            f.write(content.replace('\n', '<br/>\n'))
            f.write(f'</body>\n')
            f.write(f'</html>\n')
            print('Blog created successfully')
            return path_to_new_content
    else: # Updating the content file if it already exists
        raise FileExistsError('File already exists')


# Need to have an index page with links to all blog posts
with open(PATH_TO_BLOG/'index.html', 'r') as index:
    soup = Soup(index.read(), features="lxml")

def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get('href') for link in links)] # 1.html, 2.html, 3.html
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls

def write_to_index(path_to_new_content):
    with open(PATH_TO_BLOG/'index.html') as index:
        soup = Soup(index.read(), features="lxml")
    
    links = soup.find_all('a')

    if check_for_duplicate_links(path_to_new_content, links):
        raise ValueError('Duplicate link')
    
    link_to_new_blog = soup.new_tag('a', href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_blog.string = path_to_new_content.name.split('.')[0]
    soup.body.append(link_to_new_blog)
    soup.body.append(soup.new_tag('br'))  # Add a line break after the link

    with open(PATH_TO_BLOG/'index.html', 'w') as f:
        f.write(str(soup.prettify(formatter='html')))



write_to_index(create_blog_post('Test', 'This is a test', 'cover_image.jpg'))
update_blog()

def create_prompt(title):
    prompt = """
    Blog Post
    Title: {title}
    I'm Nir an expereinced product development leader.
    My area of expertise : AI, Product Management, and user expereince.
    
    Full text: """.format(title=title)
    return prompt

title = 'The future of Product Management in the era of AI'
prompt = create_prompt(title)

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=create_prompt(title),
    temperature=0.7,
    max_tokens=300,
)

print(response)








