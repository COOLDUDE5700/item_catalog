<h1>PROJECT : ITEM CATALOG </h1>
**This project is a part of the udacity FULL STACK DEVELOPER NANODEGREE program!**

<h2>Decription</h2>
This project is a web application ceated using the **flask** framework and supports the **CRUD** functionality for various categories and its items.

<h2>Skills utilized</h2>
1) FLASK
2) CRUD
3) OAUTH
4) PYTHON
5) HTML5
6) CSS3
7) POSTGRESQL

## Pre-Requisites :


  * **PYTHON** : Need atleast python 2.7 or a greater version.
 For downloading the latest version click [here](https://www.python.org/download/releases/3.0/)


  * **GIT** : It is a version control system (VCS) which tracks the file changes, commonly used for programming in a team setting. It can be downloaded from
  [here](https://git-scm.com/).


  * **VAGRANT** : Download and install vagrant from [here](https://www.vagrantup.com/downloads.html).
    You can configure vagrant on your machine by forking the repository :
    https://github.com/udacity/fullstack-nanodegree-vm.


 * **VIRTUALBOX** : This is a tool from oracle which enables you to run multiple
     operating systems simultaneously.
     It can be downloaded by clicking [here](https://www.virtualbox.org/)

## HOW TO RUN? :
* Using gitbash enter your vagrant directory and launch the virtual machine using the command : `$ vagrant up`

* Log in to your VM using the command : `$ vagrant ssh`

* run the app using the command : `$ python Item_catalog.py`

* The item catalog can be accessed from a browser at localhost:8079.

<h2>JSON ENDPOINTS<h2>

JSON of all items of the catalog :

JSON of a particular item in the catalog : `/catalog/<int:category_id>/item/<int:item_id>/JSON`

JSON of all the categories in the catalog :
`/catalog/categories/JSON`

JSON of the catalog : `/catalog/json`


![itemcat](https://user-images.githubusercontent.com/47191058/76146462-f6daba00-60b8-11ea-9bf7-6be34650fc05.PNG)
![itemcat2](https://user-images.githubusercontent.com/47191058/76146470-fb9f6e00-60b8-11ea-9a74-546ff1564e17.PNG)
![itemcata3](https://user-images.githubusercontent.com/47191058/76146474-fe01c800-60b8-11ea-914a-f0cbcaf727d2.PNG)

