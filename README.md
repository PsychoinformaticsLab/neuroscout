# neuroscout ⚜

To set up docker, ensure docker, docker-compose (and if on OSX) docker-machine or docker for mac are installed.

Build the containers and start the services:
     docker-compose build
     docker-compose up -d

The server should now be running. Navigate to localhost if on Docker for Mac

To access psql (and first time running, create the db), run this command (port is forwarded to host!)
    psql -h localhost -p 5432 -U postgres --password

If you make a change to /web but don't want your db to be nuked, reload like this:
    docker-compose up -d --no-deps --build web 

If you need to upgrade the db:
    docker-compose run --rm web python manage.py db migrate

Ideally, run migration scripts outside of Docker so they are tracked by git (in the future this will be forced)
    python manage.py db migrate