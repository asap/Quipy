from contextlib import contextmanager
from fabric.api import lcd, local, prefix, task
from fabric.colors import green
from fabric.contrib.console import prompt
from functools import wraps
import os

VIRTUAL_ENV = {
    'name': 'quipy',
    'path': '',
    'project_path': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'root': '$WORKON_HOME',
    'script': 'virtualenvwrapper.sh',
    '_initialized': False,
}

def initialize(function):
    """ initialize the virtual environment settings """
    @wraps(function)
    def _inner():
        """ wrapped decorator function """
        if not VIRTUAL_ENV['_initialized']:
            VIRTUAL_ENV['name'] = get_input(
                u'Name the virtual environment:',
                values=[VIRTUAL_ENV['name']],
                default=VIRTUAL_ENV['name'],
            )
            VIRTUAL_ENV['path'] = os.path.join(VIRTUAL_ENV['root'], VIRTUAL_ENV['name'])

            VIRTUAL_ENV['_initialized'] = True
        return function()
    return _inner

@task(default=True)
@initialize
def bootstrap():
    """ runs all of the setup commands """
    # Call each task
    makevirtualenv()
    pipinstall()
    projectsetup()

def get_input(message, values=None, default=None):
    """ convenience method to prompt a user for input """
    if values:
        message = '{} [{}] '.format(message, ','.join(values))

    return prompt(green(message, bold=True), default=default)

@task(alias='mkvirtualenv')
@initialize
def makevirtualenv():
    """ create the virtual environment """
    print('Making virtual environment...')
    with virtualenvwrapper():
        # Make the virtualenv...
        local('mkvirtualenv --distribute {}'.format(VIRTUAL_ENV['name']))
        with workon():
            # ... set its project folder
            local('setvirtualenvproject {} {}'.format(
                VIRTUAL_ENV['path'],
                VIRTUAL_ENV['project_path'],
            ))
            # ... automatically set DJANGO_SETTINGS_MODULE whenever it's activated
            local('echo "export DJANGO_SETTINGS_MODULE={}" >> {}'.format(
                'quipy.settings.local',
                os.path.join('$VIRTUAL_ENV', 'bin', 'postactivate')
            ))
            # ... and remove DJANGO_SETTINGS_MODULE whenever it's deactivated
            local('echo "unset DJANGO_SETTINGS_MODULE" >> {}'.format(
                os.path.join('$VIRTUAL_ENV', 'bin', 'postdeactivate')
            ))

@task(alias='install')
@initialize
def pipinstall():
    """ install the libraries found in the Pip requirements file """
    print('Installing the required libraries...')
    with virtualenvwrapper():
        with workon():
            local('pip install -r {}'.format(
                os.path.join(
                    VIRTUAL_ENV['project_path'],
                    'requirements',
                    'development.txt',
                )
            ))

@task(alias='setup')
@initialize
def projectsetup():
    """ setup the Django project """
    with lcd(os.path.join(VIRTUAL_ENV['project_path'], 'quipy',
            'quipy', 'settings')):
        local('cp example.local.py local.py')

@contextmanager
def virtualenvwrapper():
    """ use virtualenvwrapper """
    with prefix('source {}'.format(VIRTUAL_ENV['script'])):
        yield

@contextmanager
def workon():
    """ activate a virtual environment """
    with prefix('workon {}'.format(VIRTUAL_ENV['name'])):
        yield
