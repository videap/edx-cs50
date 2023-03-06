# Capstone

This application called **Plato** is an old idea that got me to start developing. This is the first version, with lots of enhancements yet to be made. It is a work-in-progress for study and full stack development.

The main idea is to connect people who need ideas with people who are creative. So, the users can buy and sell ideas very fast. The name is a "tribute" to the **World of Ideas Theory**, by Plato.

I believe this project is distinct because of the security concerns to handle sensitive data (ideas) and the payments integrations (Stripe). Some users pay, some users receive, and their capacities are handled by different "accept terms". There is a 2-layer API, one presented to the front end, and other to integrate with stripe only using data fetched from the database. Also, the user model is very robust, with protection against brute force attacks, password validation and reset options (configured with secure hashes to be sent by email), uniqueness restrictions and capacity to update user information.  


# Principles

By definition, an idea cannot be "shown" to someone before payment, otherwise the product is delivered with no payment. So the website has stripe integration that confirms payments through webkooks. There is a 2-Layer API, one for the front-end, and other for the server to handle financial operations with stripe (not accessible by clients). The information available to the client-side is very controlled.

The front-end is mostly designed with React. Lots of Classes are very alike, but they are different elements because in the future they will become very different.

Some of important features are almost ready, such as password change, webhooks, file handling, but require email servers, storage devices, public endpoints, certificates, so they are not complete yet. 

## How to Run
### Python Packages
They are all defined in the file **requirements.txt**

### Stripe API Keys
For simplicity, the project is already set with *my personal test stripe key*, and this is enough to test most features. To test the webhook, another account needs to be set, so the stripe keys must be changed. It can be done simply editing the following variables in **plato/settings.py** file:

 - STRIPE_PUBLISHABLE_KEY
 - STRIPE_SECRET_KEY

### Stripe Webhook

For a test development, *stripe test webhook* must be configured [according to this link](https://stripe.com/docs/webhooks/test).

It will install the Stripe CLI in the test environment, and to simulate the webhook, run the following command:

    stripe listen --forward-to localhost:8000/stripe_webhook
   
  > **Note:** Change "localhost:8000" accordingly, this must be a resolvable address:port to Django Server

### Stripe Credit Card for Test
To test payment options, you can use the test card for Stripe, defined by:
  4242 4242 4242 4242


## Components
All components are inside the *idea* folder.

### media/ and media/profile_images/
These folders are to maintain images and media files for the front-end (media/) and for the users image profiles (profile_images/)

### static/
This folder holds the CSS and Javascript files.

### templates/*.html files

All .html files render the HTML and some javascript code, for each page.

### /static/ideas/react_components.js
All react elements (classes) are defined here, and only that.

### api.py
Defines all functions called by the server or the front-end, mostly to manage data.

### api_stripe.py
Defines functions to interact with stripe. All functions are called by the server side, with information fetched from the database.

### forms.py
Most of the data inserted with POST requests are validated by Django using ModelForms. This file defines the classes used.  

### functions.py
General functions used by views and APIs, such as Paginator and custom validation.

#
