#Online Cook Book

This application stores food recipes. The recipes can be classified by their course type or by Dietry. A user can add as much recipes they like and keep a record of them without having the need to use paper. This application can be used from mobile devices for easy access as well. This application uses Python's Flask Framework.

##UX
This app is intended for females who love cooking. The UX is straight forward with no distractions at all. 

- As a user I want to add recipes to store them for later use.
- As a user I want to update some recipes with new information as needed.
- As a user I want to delete outdated recipes.
- As a user I want to search recipes by the course i.e. Appetizer, Breakfast, Dessert etc.
- As a user I want to track which meals are Healthy, Gluten Free, Low Carb etc.
- As a user I would like to upvote recipes of other users to appreciate them if their recipe turned out good.
- As a user I want to know how many view my recipes are getting.

##Features

- The app manages the recipes. i.e. Create, Retrive, Update, Delete
- Up vote a recipe. Go to recipe page and click upvote button.
- Views are calculated automatically 
- To filter recipes just use the list items from sidebar.

##Technologies Used

- Python/Flask
- HTML 5
- CSS 3
- Bootstrap 3
- jQuery
- Yaml Config
- MySQL Database
- Heroku

##Testing

Manual unit testing has been performed of all features. Coverage has been tested as well. 

##Deployment
The final version of app was deployed on Heroku. 

Three steps are involved

1. Freezing Requirements into Requirements.txt
2. Procfile (to run the respective Dyno)
3. Creation of runtime.txt to define the runtime.
4. Creating a Git remote for Heroku
5. Finally deploying app to master branch using "git push heroku master" command 

