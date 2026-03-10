# Using the templates from "https://github.com/tangowithcode/tango_with_django_2_code/blob/master/progress_tests/"


import os
import warnings
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class CloseButtonTests(TestCase):
    pass