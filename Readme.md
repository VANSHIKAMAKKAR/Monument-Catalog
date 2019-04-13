Indian-Monuments-Catalog

Create a Indian monuments app where users can add, edit, and delete places and monuments items in the places.
Setup and run the project
Prerequisites

    Python 2.7
    Vagrant
    VirtualBox

How to Run

    Install VirtualBox and Vagrant
    Launch Vagrant
    download vagrant files from here https://github.com/udacity/fullstack-nanodegree-vm

$ Vagrant up 

    Login to Vagrant

$ Vagrant ssh

    Change directory to /vagrant

$ Cd /vagrant

    Initialize the database

$ Python database_setup.py

    Populate the database with some initial data

$ Python lotsofmonuments.py

    Launch application

$ Python project.py

    Open the browser and go to http://localhost:5000

JSON endpoints
Returns JSON of all places

/places/JSON

Returns JSON of specific monument item

/places/<int:place_id>/loc/JSON

Returns JSON of monument

/places/<int:place_id>/<int:places_id>/JSON
