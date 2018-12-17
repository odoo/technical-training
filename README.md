# Odoo 12.0 - Technical Training: Point of Sale

## Goals

* load/store data from server
* create new UI elements (buttons, popups,...)
* modify QWeb templates

## Requirements

* [Widgets](https://github.com/odoo/technical-training/tree/12.0-15-widgets)

## PoS frontend for library

We want to create a completely new fronted for renting books. That's not the
functionality for which the PoS was designed, so we start with some easy
customizations on the frontend.

### Excercise 1: Filter displayed products & show interesting information

* Only show products that are non lost books
* Display a mark or a text if the book is not available

#### Extra task 1

* When the book is already rented, disallow adding it to the basket

### Exercise 2: Show rentals information

* On client details screen, show a list of her rentals with the related information
* Add a button to add a note on an order line, to allow to let users leave
 remarks about book's state

#### Extra task 2

* Open a popup with some book's data when clicking on a book rental

### Exercise 3: Customize receipts

* Show the return date for the rental on receipts

## Resources

### References

* [Odoo's JavaScript Reference](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html)
* [QWeb's JavaScript Reference](https://www.odoo.com/documentation/12.0/reference/qweb.html#javascript)

### Code samples

* [Load extra fields](https://github.com/odoo/odoo/blob/12.0/addons/pos_mercury/static/src/js/pos_mercury.js#L16)
* [Load extra models 1](https://github.com/odoo/odoo/blob/12.0/addons/point_of_sale/static/src/js/models.js#L1162)
* [Load extra models 2](https://github.com/odoo/odoo/blob/12.0/addons/pos_restaurant/static/src/js/multiprint.js#L45)
* [Override models](https://github.com/odoo/odoo/blob/12.0/addons/pos_restaurant/static/src/js/notes.js)
* [New popup](https://github.com/odoo/odoo/blob/12.0/addons/point_of_sale/static/src/js/popups.js)
* [New button](https://github.com/odoo/odoo/blob/12.0/addons/pos_discount/static/src/js/discount.js)
