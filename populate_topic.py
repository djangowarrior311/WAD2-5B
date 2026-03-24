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

    # a list of dictionaries with some starter tools to save us typing them all out on the site

    tools = [
        {
            'name': 'Quizlet',
            'description': 'the absolute classic flashcard app for memorizing definitions and terms before an exam.',
            'tags': ['Flashcard'],
            'link': 'https://quizlet.com',
            'score': 4.5
        },
        {
            'name': 'Notion',
            'description': 'a massive note taking and workspace app. great for organizing university modules.',
            'tags': ['Note Taking', 'AI'],
            'link': 'https://notion.so',
            'score': 4.8
        },
        {
            'name': 'ChatGPT',
            'description': 'an ai tool that is super helpful for breaking down complex maths or coding concepts.',
            'tags': ['AI'],
            'link': 'https://chat.openai.com',
            'score': 4.2
        },
        {
            'name': 'Youtube',
            'description': 'video platform that contains lots of tutorials and people to help out',
            'tags': ['Other'],
            'link': 'https://youtube.com',
            'score': 4.9
        },
        {
            'name': 'Wikipedia',
            'description': 'the largest encyclopedia',
            'tags': ['Research', 'Other'],
            'link': 'https://www.wikipedia.org/',
            'score': 4.7
        },
        {
            'name': 'Office 365',
            'description': 'a collection of apps to help with lots of different areas of learning',
            'tags': ['AI', 'Note Taking', 'Flashcard', 'Other'],
            'link': 'https://office.com',
            'score': 2.9
        },
        {
            'name': 'JSTOR',
            'description': 'a place to get scholarly articles',
            'tags': ['Research'],
            'link': 'https://www.jstor.org/',
            'score': 5.0
        }
    ]


    reviews = [
        {
            'tool': 'quizlet',
            'rating': 5,
            'review_content': 'This website helped me so much with flashcards!'
        },
        {
            'tool': 'quizlet',
            'rating': 2,
            'review_content': 'i hate this website! made me fail'
        },
        {
            'tool': 'quizlet',
            'rating': 3,
            'review_content': 'i guess this website\'s okay..'
        },
        {
            'tool': 'notion',
            'rating': 4,
            'review_content': 'This website helped me so much with note taking!'
        },
        {
            'tool': 'notion',
            'rating': 1,
            'review_content': 'full of ai slop'
        },
        {
            'tool': 'notion',
            'rating': 3,
            'review_content': 'goodnotes and obsidian are wayyyy better'
        },
        {
            'tool': 'notion',
            'rating': 2,
            'review_content': 'not sure what to write for this review...'
        },
        {
            'tool': 'chatgpt',
            'rating': 1,
            'review_content': 'ujkdadakljgdafkl'
        },
        {
            'tool': 'chatgpt',
            'rating': 2,
            'review_content': 'i hate this website! made me fail'
        },
        {
            'tool': 'chatgpt',
            'rating': 3,
            'review_content': 'i guess this website\'s okay..'
        },
        {
            'tool': 'youtube',
            'rating': 5,
            'review_content': 'youtube helped me so much with flashcards!'
        },
        {
            'tool': 'youtube',
            'rating': 2,
            'review_content': 'i hate youtube! made me fail'
        },
        {
            'tool': 'youtube',
            'rating': 3,
            'review_content': 'i guess youtube is okay..'
        },
        {
            'tool': 'wikipedia',
            'rating': 5,
            'review_content': 'wikipedia helped me so much with flashcards!'
        },
        {
            'tool': 'wikipedia',
            'rating': 2,
            'review_content': 'i hate this website! made me fail'
        },
        {
            'tool': 'wikipedia',
            'rating': 3,
            'review_content': 'i guess this website\'s okay..'
        },
        {
            'tool': 'office-365',
            'rating': 5,
            'review_content': 'office 365 helped me so much with flashcards!'
        },
        {
            'tool': 'office-365',
            'rating': 2,
            'review_content': 'i hate this website! made me fail'
        },
        {
            'tool': 'office-365',
            'rating': 3,
            'review_content': 'i guess this website\'s okay..'
        },
        {
            'tool': 'jstor',
            'rating': 5,
            'review_content': 'jstor helped me so much with flashcards!'
        },
        {
            'tool': 'jstor',
            'rating': 1,
            'review_content': 'i hate this website! made me fail'
        },
        {
            'tool': 'jstor',
            'rating': 4,
            'review_content': 'i guess this website\'s okay..'
        }
    ]

    # now we loop through our list and actually inject them into the database

    for tool_data in tools:
        t = add_tool(tool_data, dummy_user)
        print(f"successfully added tool: {t.name} with tags {t.tags}")

    for review in reviews:
        tool = LearningTool.objects.get(slug=review['tool'])
        t = add_review(review, dummy_user, tool)

def get_tags(tool_data):
    tags = []
    for tag in tool_data['tags']:
        t = Tag.objects.get_or_create(
            name=tag
        )[0]
        t.save()
        tags.append(t)
    return tags

# a quick helper function to keep the main loop clean
def add_tool(tool_data, user):
    t = LearningTool.objects.get_or_create(
        name=tool_data['name'],
        creator=user
    )[0]
    
    t.description = tool_data['description']
    t.tags.set(get_tags(tool_data))
    #t.tags = tool_data['tags']
    t.link = tool_data['link']
    t.score = tool_data['score']
    t.save()
    return t

def add_review(reviews, _user, _tool):
    t = Review.objects.create(
        user = _user,
        tool = _tool
    )
    t.rating = reviews['rating']
    t.review_content = reviews['review_content']
    t.save()
    return t

# this line just makes sure the script only runs when we tell it to in the terminal
if __name__ == '__main__':
    populate()
    print("population complete! your database is full.")