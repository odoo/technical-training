# Odoo 12.0 - Technical Training

This branch contains the training material for the Odoo Javascript Training.

Here is what you will find:

* Slides
    * [Introduction slides for day 1](training_slides_day1.pdf)
    * [Introduction slides for day 2](training_slides_day2.pdf)
* Odoo Addons
    * [awesome_tshirt](awesome_tshirt/) a basic addon to play with for this training
    * [awesome_map](awesome_map/) a basic (non functional) addon to add a map view in Odoo
* Exercises
    * [Exercises, part 1](exercises_1.md) Widgets
    * [Exercises, part 2](exercises_2.md) Advanced JS
    * [Exercises, part 3](exercises_3.md) Creating a new view
    * [Exercises, part 4](exercises_4.md) Testing


## Requirements

* Moderate knowledge of Odoo
* Moderate knowledge of Javascript


## Scenario

We are the IT staff for the Awesome T-Shirt company, which is in the business of
printing customised tshirts for online customers.

The usual process is the following: a customer looking for a nice t-shirt can
simply order it on the Awesome T-Shirt website, and give the url for any
image that he wants.  He also has to fill some basic informations, such as the
desired size, and amount of t-shirts.  Once he confirms his order, and once the
payment is validated, the system will create a task in our project application.

The project is a simple kanban view, with a few columns.

The Awesome T-shirt big boss, Bafien Ckinpaers, is not happy with our
implementation. He believe that by micromanaging more, he will be able to
extract more revenue from his employees.

As the IT staff for Awesome T-shirt, we are tasked with improving the system.
Various independant tasks need to be done.


## Starting point

- *awesome_tshirt*: this is an addon which implements the business flows/features
  for our fictional company.  It contains a few controllers, templates, files to
  ease the training.
- *awesome_map*: this is an (incomplete) addon which will be used as a basis to
  create a new view from scratch.

The goal of this training is to play with the code and to learn! So, do not be
afraid to experiment...