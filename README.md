# Item Catalog Project 
This project is created as a part of Udacity Full-stack Nano degree Program.
It is a item catalog. Where All the catagory and sub items are displayed. 
CRUD operations are implemented.

# Technology
  Python
  Flask
  Vagrant
  SQLAlchemy
  HTML
  CSS
  BootStrap

# Functionality
API Endpoints : The project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog.
CRUD: Read : Website reads category and item information from a database.
CRUD: Create : Website includes a form allowing users to add new items and correctly processes submitted forms.
CRUD: Update : Website does include a form to edit/update a current record in the database table and correctly processes submitted forms.
CRUD: Delete : Website does include a function to delete a current record.
Authentication & Authorizatio : Create, delete and update operations do consider authorization status prior to execution. Page implements a third-party authentication & authorization service (like Google Accounts ) instead of implementing its own authentication & authorization spec.


# Access and test application by visiting http://localhost:8000 locally

# To Run
Go to Vagrant Folder.
If you need to bring the virtual machine online:

  vagrant up
  
Then log into it with

  vagrant ssh
  
Once machine is up and running

  cd /vagrant/ItemCatalog
  
To set up database and populate it

  python CatalogDB.py
  

# Database :
User : Includes information about User
Catalog : Includes information about Catalog 
CatalogItem : Includes information related to Catalog item, related Catalog entry and user who created it.
  
