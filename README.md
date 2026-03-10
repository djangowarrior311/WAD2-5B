# Getting started:
We'll be using anaconda because university machines like it.
## Creating the environment
1. Open `Anaconda Prompt`
2. ```conda create -n topic python=3.11```
3. ```pip install pillow```
4. ```pip install django==2.2.28```
5. ```pip install selenium``` <-- for tests
## Getting the project
6. Navigate to your working directory
7. ```git clone "https://github.com/MrSkroob/WAD2-5B"```
8. CD into the new WAD2-5B.
## Running the project:
9. CD into the `topic` folder. 
10. `python manage.py runserver` and open link `http://127.0.0.1:8000/` to check everything is running correctly.
# Housekeeping:
- Please commit as often as possible.
```
git add *
git commit -m "commit message"
git push
```
- Follow PEP when you can (snake_case for most things, CONSTANT_CASE for constants, PascalCase for classes)
- Test everything! Take a look at the Django testing code for some templates. 
- If you have some naming conventions/code styling of in your branches, please add them to this readme.
