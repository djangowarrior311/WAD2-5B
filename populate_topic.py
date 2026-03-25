import os

# this line hooks the script up to project's settings so it knows where the database is
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topic_project.topic_project.settings')

import django
django.setup()

# importing the tables from models.py file
from topic_project.topic.models import LearningTool, Review, Tag
from django.contrib.auth.models import User

def populate():
    print("starting the topic population script...")
    
    # first, let's make a fake user to own these tools since the database requires a creator
    # get_or_create means it won't crash if we run this script twice!
    dummy_user, created = User.objects.get_or_create(username='admin_syon', email='admin@topic.com')
    if created:
        dummy_user.set_password('neon_highlighter123')
        dummy_user.save()

    tags = LearningTool.CATEGORIES

    # a list of dictionaries with some starter tools to save us typing them all out on the site
    tools = [
        {
            'name': 'Quizlet',
            'description': 'the absolute classic flashcard app for memorizing definitions and terms before an exam.',
            'category': 'FLASH',
            'link': 'https://quizlet.com',
            'score': 4.5
        },
        {
            'name': 'Notion',
            'description': 'a massive note taking and workspace app. great for organizing university modules.',
            'category': 'NOTE',
            'link': 'https://notion.so',
            'score': 4.8
        },
        {
            'name': 'ChatGPT',
            'description': 'an ai tool that is super helpful for breaking down complex maths or coding concepts.',
            'category': 'AI',
            'link': 'https://chat.openai.com',
            'score': 4.2
        }
    ]

    # now we loop through our list and actually inject them into the database
    for tool_data in tools:
        t = add_tool(tool_data, dummy_user)
        print(f"successfully added tool: {t.name}")

    for tag in tags:
        add_tag(tag[0])


def add_tag(tag_name: str):
    t = Tag.objects.get_or_create(
        name=tag_name
    )[0]

    t.save()
    return t


# a quick helper function to keep the main loop clean
def add_tool(tool_data, user):
    t = LearningTool.objects.get_or_create(
        name=tool_data['name'],
        creator=user
    )[0]
    
    t.description = tool_data['description']
    t.category = tool_data['category']
    t.link = tool_data['link']
    t.score = tool_data['score']
    t.save()
    return t

# this line just makes sure the script only runs when we tell it to in the terminal
if __name__ == '__main__':
    populate()
    print("population complete! your database is full.")