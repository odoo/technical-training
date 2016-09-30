# Modify Business Flows

## Goal

In this module, you will learn to modify existing business flows.

## Requirements

* [Model Inheritance](../04-model-inheritance)
* [View Inheritance](../05-view-inheritance)


## Problem 1: Double Validation on Sales Orders

Create a small module that depends on the module `sale`. The module should add a
double validation process on sales orders. Add a state on model `sale.order`,
and modify buttons so that the salesperson first confirms their sales order,
then let their manager double confirm it. Only the second confirmation should
assign the sales order to the state `sale`.

### References

* [Sales Order](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/addons/sale/models/sale.py#L15)
* [Selection Fields](https://github.com/odoo/odoo/blob/76c443eda331b75bf5dfa7ec22b8eb22e1084343/odoo/fields.py#L1625)
