
Design Documentation

Login (Maya)
Ensures the user enters a valid username and password, and if so, logs them in. This allows users to have personal accounts, with favorites and private messages.

Register (Maya)
Ensures that the user enters a unique username via JavaScript, and makes sure that the password and the confirmation password are the same and at least eight characters via python. The password is then hashed for security, and the username, hash, name of user and email of the user are inserted into the users table. The name of user and email of the user are taken for possible future additions.

Home (Maya and Brittney)
In python, we generated a list of the locations the user has added or rates and a list of locations they have favorited. We put these in drop-down forms that, when selected and submitted, can look up the chosen location. This way the user can see what places they found important, and can easily look them up to learn what others think. This is on the homepage because we thought it was the most useful information and the one that users would want to see first before delving further into the site.

Add (Maya)
When this function is called with the GET method a form with different categories is made. Most categories have a drop down with a list of choices so we can control and limit the input values so they are easier to manipulate. We implemented JavaScript so that two locations can’t be entered twice. Using JavaScript we required the user to fill out the entire form to ensure we have enough data. With the POST method, the information entered is inserted into the locations table and foreign keys for the location name and user are put in the key table to save memory.

Rate (Maya)
This function is similar to Add, only instead of entering the location’s name as text the user must choose from a drop-down list of all the locations in the database. They same the HTML for the forms that they share to be efficient. Again we used JavaScript to require the user to fill out the entire form to ensure we have enough data. Similarly, with the POST method, the information entered is inserted into the locations table and foreign keys for the location name and user are put in the key table to save memory.

Favorite (Maya)
When this function is called with the GET method a list of all places the users have rated or added in the database and all the places that the user has not yet favorited are generated and put into two forms with dropdown lists. The user can then look up places they have rated, or favorite places they have not yet favorited. This is done by inserting the location into the favorite table using foreign keys for the locations and the user to save memory. The page is then regenerated with the location favorited now it the favorites list. This function lets the user can keep track of locations they prefer to study and can find out the latest information about them.

Recent (Maya)
This function generates a list of seven or less of the latest ratings to be inputted. The id of the ratings in the locations table is automatically generated in numerical order. Thus we took the highest seven id numbers and put all of their associated information into a list, that is then turned into a table in HTML. The user can see the most recent opinions of their peers, without being overloaded with all the ratings in the database.

Sort By (Maya and Britteny)
When this function is called with the GET method a form with a drop-down or all the different locations and a dropdown of numerical ratings is made. Once the location and rating are submitted, every location is iterated through, lists are made of the values in each category, and then the location’s average value for each category is produced. Using if statements to choose which category the user selected if the average is greater than or equal to the number the user choose, it will be added to a list of locations. This list is then generated in HTML.

Lookup (Britteny)
This function generates a drop-down selector that contains all of the added locations when called with the GET method. Once you submit the form you are taken to the location HTML that shows the average ratings as well as the breakdown of activities done there and any comments that were left. The averages are calculated using a list averaging function that averages lists that I created bt iterating through the database. I was able to get a count of each activity by performing the COUNT operation on the location database.

Meetings (Ahmed)
This function collects information for meetings through an HTML page that takes in the location, date, time, and meeting information. The function utilizes Python and Jinja in order to connect the location field to the list of Locations that have been added allowing the user to select locations from a drop-down. Python inserts the information into a data table called meetings which stores this information, and the user is redirected to the Meeting List page.

Meetings List (Ahmed)
When called with the GET method the function SELECTs the information from the meetings table and through the use of HTML and Jinja the information is displayed in a table on the Meeting List page of the web application. The meeting table is styled using Javascript and Bootstrap. These enhance the appearance of the table as well as allowing the table to be sorted.

Messages (Ahmed and Maya)
When called with the GET method the function SELECTs all the usernames in the system and renders them in a dropdown list in HTML. This way users canot send a message to a user who does not exist. They can then submit their text message. When called with a POST method, the foreign key associated with the recipient’s username is SELECTed. Then the message with this key and the sender's key is INSERTed into the database. The use of foreign keys saves memory space.

Inbox (Ahmed and Maya)
This function creates an HTML table with all messages sent to the user. The python SELECTs all the rows where the recipient is the current user. These messages are iterated through to create a list of sender names from the id number associated with the sender so their names will appear on the table. These lists are sent to the HTML file to create the table. JavaScript allows the user to sort the table, and tells the user that they have have no messages rather than filling the table if the list of messages, called mail, is empty.







