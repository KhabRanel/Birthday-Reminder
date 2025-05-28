import os
import sys
import django


# Переходим в корень проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birthday_project.settings")

django.setup()