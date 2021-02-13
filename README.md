# Simple Django Elasticsearch project inside a Docker container using Cookiecutter 


I used Django framework to design my API 

I used [cookiecutter](https://github.com/pydanny/cookiecutter-django) to benefit from their easy setup for Docker(Optional)

I used [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/brew.html) to benefit from rapid full-text search 


# The Steps
You need to pass an Excel file in order to put data into your Elasticsearch

You can pass the file through a signed link (Optional)

You may clean the file before transferring it to Elasticsearch

You load your data into Elasticsearch

You call your API to search through your data using Elasticsearch query

# Flexibility

You can have different data and search for different fields and look for different results.

I provide you with this [sample](https://github.com/Morvarid/django_elasticsearch_docker/blob/master/sample_file.xlsx)


I have included a Postman collection for ease of use.  The collection can be found in the root of this repo:

    salary_api.postman_collection.json

# Setup

If you are using cookiecutter and want to use a container, install Docker if you have not done so already.

You will need to have the .xlsx file hosted somewhere that is publicly available as you will post a link to that file into the running container.  
Posting this file will bring the file down locally.

* Optional: 
    * You may modify the code if you have a csv file instead. 
    * you can have your file located somewhere in your system but again you need to modify the code.



# How to run

Clone this repo and cd into that directory

The following project is configured to run in a Docker container.

Build and launch Docker.

     docker-compose -f local.yml build

     docker-compose -f local.yml up
     

if you are not using Docker and you are running it locally you need to install Elasticsearch.

# Test Upload API


As mentioned above, you may execute the import by running the Postman call

     upload file to Elasticsearch

This will take some time to run depending how big your file is.

Path: 

    /v1/upload?link=
    
   

# Test search API

Once the import is complete you may hit the search endpoint.

Run the postman call

     API or getting salary info
Path:

    /v1/search
        
API JSON request:


    {
    "title": "engineer",
    "location": "los angeles" 
    }


API response:

    {
        "number of datapoints": 5450,
        "mean salary": 156840.6,
        "median salary": 105225.6,
        "25% percentile salary": 81933.9,
        "75% percentile salary": 130803.9
    }


# Scalability
Ideally this is a task that should be sent to a message queue and have a process tracker so the state of the process is complete.
If this project is part of your Data Pipeline, you may consider using Celery and RabbitMQ/Redis to speed up the process of digesting the file and importing it to Elasticsearch.
If your file is huge, over 250 MB, you may consider using Multithreading. 





