# Module 17: Creating new views


## Goal

* learn how to create new view from scratch
* understand how to interact with the control panel

## Starting point

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


Step 2: create a module from scratch, called 'awesome_map'.  Add the structure to register a new view type (look at web_grid for an example)

Step 3: make sure you add the map view in the customer actions, and start by rendering some static content

Step 4: in your new map view, fetch the records for the current domain/context

Then display a map centered on the current location

And add all the pins at the correct location

And add a rendering for the custom template in the arch

And make sure the url is updated.  And if you modify the search view, it should be updated.


Extra task: clicking on a pin open the customer in a form view

Extra task: add a button in the control panel to center the map on the current location

Extra task: add a button in the control panel to geolocate the partner (there is already a geolocate button somewhere, base_geolocalize) (move this to next module???)

### References

- geolocation API (see MDN)
- leafletjs to display a map?