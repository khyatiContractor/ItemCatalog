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


## Access and test application by visiting http://localhost:5000 locally

VirtualBox
VirtualBox is the software that actually runs the VM. You can download it from virtualbox.org. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from vagrantup.com. Install the version for your operating system.

Fetch the Source Code and VM Configuration

Fork the starter repo Log into your personal Github account, and fork the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

Clone the remote to your local machine From the terminal, run the following command (be sure to replace with your GitHub username): git clone http://github.com//fullstack-nanodegree-vm 

This will give you a directory named fullstack that is a clone of your remote fullstack-nanodegree-vm repository.

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
 
To run project

    python project.py
    
    visit : http://localhost:5000 in your browser
  

# Database :
User : Includes information about User
Catalog : Includes information about Catalog 
CatalogItem : Includes information related to Catalog item, related Catalog entry and user who created it.
  
