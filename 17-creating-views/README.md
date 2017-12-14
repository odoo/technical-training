# Module 17: Creating new views


## Goal

* learn how to create new view from scratch
* understand how to interact with the control panel

## Starting point

* [Library app from 'Advanced Customization'](../advanced-customization)
* [Map skeleton application](./awesome_map)

## Problem 1: Our very own Map view (Library)

To deliver an awesome customer service, we want to know more about where our customer lives. In this module, we will create a map view from scratch.

The arch should look like this:

    <map latitude="some_field" longitude="some_other_field">
        <field name="field1"/>
        <field name="field2"/>
        <template>
            <div>... <t t-esc="record.field1"/>
            </div>
        </template>
    </map>

In this code, the latitude and longitude attributes should describe a float field. The template tag is a small qweb template, which should be rendered on a marker at the corresponding record location.  The field tags determine which fields should be fetched.

- install the awesome_map module
- add the map view in the customer action
- create a new JS module 'awesome_map.MapView', and register AbstractView to view registry
- implement a map view, renderer, controller and model...

### Extra tasks

- clicking on a pin open the customer in a form view
- add buttons in the control panel to zoom in and out


## Resources

### References

* [Leaflet.js](http://leafletjs.com/)