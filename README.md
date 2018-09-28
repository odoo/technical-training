
![Odoo Logo](https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo_small.png)

# Odoo 13.0 - Technical Training

This branch contains the training material for the Odoo Javascript Training.
This training focus on various interesting changes that can be done on the web
client user interface.

The goal of this training is to play with the code and to learn! So, do not be
afraid to experiment...

## Requirements

* Moderate knowledge of Odoo
* Moderate knowledge of Javascript
* working machine properly setup for development purpose
* basic knowledge of git is a bonus


## Scenario

For this training, we will put ourselves in the shoes of the IT staff for the
fictional Awesome T-Shirt company, which is in the business of printing
customised tshirts for online customers.

The usual process is the following: a customer looking for a nice t-shirt can
simply order it on the Awesome T-Shirt website, and give the url for any
image that he wants.  He also has to fill some basic informations, such as the
desired size, and amount of t-shirts.  Once he confirms his order, and once the
payment is validated, the system will create a task in our project application.

The Awesome T-Shirt company uses Odoo for managing its orders, and built a
dedicated odoo module to manage their workflow. The project is currently a
simple kanban view, with a few columns.

The Awesome T-shirt big boss, Bafien Ckinpaers, is not happy with our
implementation. He believe that by micromanaging more, he will be able to
extract more revenue from his employees.

As the IT staff for Awesome T-shirt, we are tasked with improving the system.
Various independant tasks need to be done.

The current starting point for this training is contained in this repository.
We have two Odoo modules:

* [awesome_tshirt/](awesome_tshirt/) this is an addon which implements the business
flows/features for our fictional company.  It contains a few controllers, templates
and files to start the training.
* [awesome_map/](awesome_map/) a basic (incomplete) addon to add an awesome
map view in Odoo (starting point for module 3)

## Resources

* Slides
    * [Introduction slides for day 1](training_slides_day1.pdf)
    * [Introduction slides for day 2](training_slides_day2.pdf)
* Exercises
    * [Exercises, part 1](exercises_1.md) Widgets
    * [Exercises, part 2](exercises_2.md) Advanced JS
    * [Exercises, part 3](exercises_3.md) Creating a new view
    * [Exercises, part 4](exercises_4.md) Testing


## Integration with Odoo.sh

To deploy the current state of this branch to Odoo.sh, you can click
<a href="https://www.odoo.sh/app/add/?name=13.0-20-javascript-training&author=ged-odoo&url=https%3A%2F%2Fgithub.com%2Fodoo%2Ftechnical-training%2Farchive%2F13.0-20-javascript-training.zip&free=1&version=13.0&icon=https%3A%2F%2Fapps.odoo.com%2Fapps%2Ficon_image%3Fmodule_id%3D52346">here</a>.



