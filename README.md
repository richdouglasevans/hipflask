_Hipflask_ is an example application capturing my common
[Flask](http://flask.pocoo.org/) and [AngularJS](https://angularjs.org/)
practices.

## Development Environment

You'll need the following for your development environment:

1. [Python](http://www.python.org/)
2. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)
3. [Vagrant](http://vagrantup.com)
4. (_optionally_) [PyCharm](https://www.jetbrains.com/pycharm/)

### Local Setup

#### 1. Clone the project:

    $ git clone https://github.com/richdouglasevans/hipflask.git
    $ cd hipflask

#### 2. Create and initialize virtualenv for the project:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

#### 3. Start the virtual machine:

    $ vagrant up

#### 4. Load sample data:

    $ python data.py

#### 5. Run the development server:

    $ python wsgi.py

#### 6. Open [http://localhost:5000](http://localhost:5000)

### Development

If all went well you'll be ready to start hacking away on the application.

#### Tests

I use [Nose](https://nose.readthedocs.org/en/latest/).

    $ nosetests

