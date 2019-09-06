# product-api [![Build Status](https://travis-ci.com/JustinDearden/product-api.svg?branch=master)](https://travis-ci.com/JustinDearden/product-api)
### A rest API in Django   
The API supports   
* Creating user accounts  
-- User registration with auth token creation  
-- Entries can be stored into a database   
--- Database values are listed inside `app/settings.py` & `docker-compose`  
* Create and store new products  
-- Products, Attributes, Tags & Users all have unit testing to ensure they can be created. The Travis build has all the details of the tests   
* Add tags to products & filter based on them  
* Add attributes to products that extend to search criteria  

## Docker  
The container uses port 8000  

### Docker Commands  
`docker-compose run --rm app sh -c "python manage.py test && flake8"`   
-- Runs testing locally  

`docker-compose up`  
-- CD into the directory and run the above command to activate the container  

#### If you edit the models or need to create a new local super user  
`docker-compose run --rm app sh -c "python manage.py makemigrations core"`  
-- the `core` app is where all the base models are stored for the API, the above command specifies that app name   

`docker-compose run --rm app sh -c "python manage.py createsuperuser"`  
-- Creates a new local super user  

## Accessing the site & URL paths   
Access the site at `http://127.0.0.1:8000`   
-- There is no default template installed to you will see a `Page Not Found (404)` error on loading it   
-- Admin and the API pages can still be accessed along with the rest framework   

#### Admin Login   
`http://127.0.0.1:8000/admin/login/`   
-- You will need to create a super user locally or on the DB before being able to sign in   

#### API Pages   
-- Each pages displays and allows for editing / creation of new (products/attributes/tags)   

##### Create User Token    
`http://127.0.0.1:8000/api/user/token/`   
-- Create and see a user auth token - one is required to gain access to the other API pages   
-- [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en) is a good plugin for managing user auth tokens    

##### API Root    
`http://127.0.0.1:8000/api/product/`  

-- Product List   
`http://127.0.0.1:8000/api/product/products/`   

-- Attributes List   
`http://127.0.0.1:8000/api/product/attributes/`   

-- Tags List   
`http://127.0.0.1:8000/api/product/tags/`   
