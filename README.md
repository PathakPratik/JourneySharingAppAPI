# Running the app locally

Make sure that you have no pre existing running mysql or journey_sharing_app container

Change the directory to SQL-Docker, in this folder, you find a Dockerfile used for creating the image and running the mysql container by running this command:

```
cd SQL-Docker
docker build --tag mysql_container:1.0.0 .
```

Change the directory to WebSocketServer, in this folder, you find a Dockerfile used for creating the image and running the socket server container by running this command:

```
cd WebSocketServer
docker build --tag web_socket_server:v1 .
```

Build the image for the Load Balancer as well 
```
cd LoadBalancer 
docker build -t loadbalancer:v1 . \\ add --platform=linux/amd64 if on apple silicon Mac 
```

Then go back to the main Directory and run:

```
cd .. \\ go back to root directory if not already there
docker build -t journey_sharing_app:v1 .
```

After building, run the app by running:

`docker-compose up`

The app will then start, be patient, it will fail in the first 5 attempts (maybe more in your machine) as the db and mysql container has to be set up. The app will then automatically restart and eventually connect to the database.

# How to run test cases in docker

To run the test cases, you first need to run the project using the guideline above. Then, go to setup.py and change the test_mode to True

`test_mode = True`

Open a new Terminal and run

`docker container list`

Copy the container id which its name is journeysharingappapi_api_1. replace the container id you copied with the one in command below, Then run 

`docker exec -it container_id bash`

make sure that pytest and coverage packages are installed by running:

`pip install pytest`
`pip install coverage`

Navigate to tests directory by

`cd tests`

Run the test cases by ruuning the command below:

`coverage run -m pytest`

After finishing the operation, run command below to see the coverage report:

`coverage report`

If you want to use the GUI for coverage, run:

`coverage html`

This will create a folder under tests directory called htmlcov, open the index.html file in your browser to see the coverage of the test cases line by line within the project.

Make sure that you will change the test_mode in the setup.py to False after finishing the testcases.







