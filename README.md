# Running the app locally

Make sure that you have no pre existing running mysql or journey_sharing_app container

Change the directory to SQL-Docker, in this folder, you find a Dockerfile used for creating the image and running the mysql container by running this command:

`docker build --tag mysql_container:1.0.0 .`

Change the directory to WebSocketServer, in this folder, you find a Dockerfile used for creating the image and running the socket server container by running this command:

`docker build --tag web_socket_server:v1 .`

Then go back to the main Directory and run:

`docker build -t journey_sharing_app:v1 .`

After building, run the app by running:

`docker-compose up`

The app will then start, be patient, it will fail in the first 5 attempts (maybe more in your machine) as the db and mysql container has to be set up. The app will then automatically restart and eventually connect to the database.

# How to run test cases

`pytest`
