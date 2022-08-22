# Recipes website
#### Video Demo:  <https://www.youtube.com/watch?v=RJIzR0e-alk&ab_channel=NielsOudenampsen>
#### Description
This is my final project of the CS50 course. I designed an application where users can search for all the recipes from the Tasty website. They are also able to view recipes and add them to their favorite recipes list. The project uses the following programming languages (and frameworks):
- Python (Flask)
- SQL
- JavaScript (AJAX)
- HTML
- CSS (Bootstrap)

#### How to Install and Run the Project?
- Make sure you are in the root folder of the project by executing this command: ```pwd``` (You need to be in the project folder).
- For Windows Powershell set the API key with the system envirmental variable by executing this command:  ```$env:API_KEY=value```.
- For Linux Bash set the API key with the system envirmental variable by executing this command:  ```export API_KEY=value```.
- Run the application by executing this command: ```python3 application.py```.
- The application is started when you see the following text in the terminal: ``` * Running on http://127.0.0.1:5000```.

#### List of the files I wrote
* Main
  * application.py
  * helper.py
  * recipe.db
  * README.MD
 
* Templates
  * index.html
  * layout.html
  * register.html
  * login.html
  * change-credentials.html
  * my_recipes.html
  * recipe_detail.html

* Static
  * 404.webp
  * main.js
  * styles.css

#### Explaination of the files I wrote
##### application.py
This file is called when starting the program. At the top of the file are all the imports of the dependencies needed for this project. After that the Flask app is initialized. The Jinja templating filters are set. The app's cookies method is set to use the filesystem and the sessions created are temporary. The database connection is established. All the routes of the application are specified and marked with a decorator if a login is required.

##### helpers.py
This file has all the functions needed for the application.py file and also the functions needed for the custom Jinja filters. The main function of the whole application is: lookup_recipe(start,size,tag,query). This function takes four arguments needed for the tasty API hosted on rapidapi.com. The API gives back a JSON object with all the recipes found. The recipes contains a lot of information. For simplicity are in this application only the following attributes used: id, name, description and image.

(In the first implementation the function made a API request for each call of the function. After making the mistake of calling the function in an infinite loop the API I was using blocked me for one month. My solution for this problem was to cache the result of the API in the database.)

##### recipe.db
This is the database file used for this application. There are two tables in the database. The recipes table contains the search string with the corresponding JSON response (used for the caching functionality). The users tables contains information about the users of the application.

##### index.html
This is the main page of the application after the user is logged in. All the favorites of the user are displayed in a carousel. Above that the user is able to search for recipes.

##### layout.html
This is the main layout of the application all the other templates are using. All the default boilerplate code for setting up a HTML website is present.

##### register.html
This template is used for regrister a new user to the application.

##### login.html
This template is used for the login of a user into the application.

##### change-credentials.html
This template is used for changing the credentials of the logged in user.

##### my_recipes.html
This template is used for displaying and updating all the favorites of the logged in user.

##### recipe_detail.html
This template is used for displaying all the detailes of a single recipe.

##### 404.webp
This is the image used for displaying to the user that there is noting found.

##### main.js
This is the main JavaScript file used for this application. There are three main functions in this file. The first function in this file is called when the user clicks on the favorite button. The CSS off the grey favorite star is changed to yellow in the frontend. In the backend the function is making a post-request via the AJAX technique. This is the only way to make a POST request in the backend and letting the user know that they made a change, without reloading the page.

##### styles.css
This file contains the custom styles used for this project. The main styles used for this project are from the Bootstrap framework.
