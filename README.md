### Virtual environment configuration

    $ cd scripts
    $ fab

Additional information can be found by running `$ fab --list`

_From the commit logs:_

> This is a fabric script that can be used to create and initialize a virtual environment. In order for the script to work, virtualenv, virtualenvwrapper, and fabric must be installed.

    $ pip install -U virtualenv virtualenvwrapper fabric

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
