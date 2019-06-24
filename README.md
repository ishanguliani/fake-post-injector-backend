chrome extension that performs fake post injection in Facebook timeline

To fire up the server have `python3` and `pipenv` installed.

### open terminal and cd to the project root directory 
#### start virtual environment
`pipenv shell`
#### install dependencies
`pipenv install`
#### set up database locally
`python3 manage.py makemigrations`
`python3 manage.py migrate`
#### set up static files locally
`python3 manage.py collectstatic`
#### start the server
`python3 manage.py runserver`
