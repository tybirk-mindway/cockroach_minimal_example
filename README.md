# cockroach_minimal_example

First, you need to configure environment variables to point to the right database and if necessary include a certificate. 
Then, you should be able to just run 

> docker-compose up --build 

to run the main.py file and insert data. In db.py and db_models.py you can change the variable "USE_SQLITE" to try the same with sqlite and observe a tremendous speed difference.
