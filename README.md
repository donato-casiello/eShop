# eShop
eShop is a e-commerce site designed in Django  that allow users to buy a different kinds of products, grouped into categories. Payments are managed by **Stripe**.

### Features
* **Home**: are shown all the products, paginated by 10, in chronological order (latest product insert into database is on the top);
* **Product detail**: clicking on product image or title, the users are redirect to product detail page that shows the main image, other images, product price and product discount price (if exists), title, brief description and additional informations;
* **Category**: users can search a specific category of products;
* **Search**: users can search specific name of product; the search page also shows results that contain the query, not just the exact query;
* **Profile**: users can edit their own profile page, with additional information like first name, last name, phone number, etc.;
* **Cart**: shows all the products that the users added in their carts. To see the cart a user has to be logged in;
* **Order summary**: summary of what the user has added to the cart with the total to be paid;
* **Checkout**: last step before payment, where the user must enter the information necessary for the delivery of the products;

### Getting Started
1. Install [python3](https://www.python.org/downloads/), [pip3](https://pip.pypa.io/en/stable/installing/)
2. Active `v-shop` virtualenv
3. Install dependencies from requirements.txt 

    ```
    pip3 install -r requirements.txt
    ```
   
4. Run Server 
    ``` 
    python3 manage.py runserver
    ```
5. check `127.0.0.1:8000`


