### Virtual environment configuration

    $ cd scripts
    $ fab

Additional information can be found by running `$ fab --list`

_From the commit logs:_

> This is a fabric script that can be used to create and initialize a virtual environment. In order for the script to work, virtualenv, virtualenvwrapper, and fabric must be installed.

    $ pip install -U virtualenv virtualenvwrapper fabric

You can then import quotes from [The Movie Quotes
Database](http://www.moviequotedb.com) with the "scrape" command:

    $ ./manage.py scrape monty-python-and-the-holy-grail

The argument is the "short name" of the movie as found in the URL of a page
at The Movie Quote Database's website.

## Heroku

    $ heroku create --stack cedar --buildpack git@github.com:cbslocal/heroku-buildpack-python.git [name]

    $ heroku create --stack cedar --buildpack git@github.com:cbslocal/heroku-buildpack-python.git --remote staging [name-staging]
    $ heroku config:add DJANGO_DEBUG=True --remote staging

### Deployment

_Production_

    $ git push heroku master

_Staging_

    $ git push staging develop:master

For further reading, see [Managing Multiple Environemnts for an App](https://devcenter.heroku.com/articles/multiple-environments)
