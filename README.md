# Game Finder
#### Video Demo:  <https://youtu.be/1jrxqPDxLkc>
#### Description:

My name is Anisha Rahut, I am 16 years old, and I reside in Saratoga, California, USA. For my CS50 Final Project, I created a web page called "Game Finder," which allows soccer players to create and join games online so that they can then play in person. Users may either create their own requests or choose from a selection of other users' requests to create a game. This web application is built using Bootstrap, Python, SQL, and HTML.

The project aims to provide a platform for soccer enthusiasts to organize and participate in real-life games. To get started, users need to register by providing their email, password, password confirmation, city, and state. This information is stored in the users' table that is organized by user_id.

Once registered and logged in, the site directs users to the home page featuring a user-friendly interface where players can input their name, location, and start and end times to create a game request. The back end of the site stores this information in a SQLite table called requests which is also organized by user_id.

The “find” tab allows users to view outgoing requests and choose one that is convenient to them. These requests are displayed in a user-friendly manner and a user must simply click select to choose a request. The details of each game, such as the name, location, start and end times, and the player who initiated the request is displayed. By choosing a game request that suits their availability and preferences a game is thus formed.

The "games" tab provides a comprehensive overview of all ongoing games on the platform. Users can view the current score, the names of participating players, and their contact information. However, to address privacy concerns and improve security, future improvements of the platform can implement access restrictions to ensure that only the current user can view information about other users.

The platform also includes a "score" tab that enables users to update the score of their ongoing games. By entering the game number (corresponding to the game on the "games" tab) and the goals scored by players 1 and 2, users can submit the score. This feature encourages fair play and allows players to track their progress within the community.


In conclusion, Game Finder offers a user-friendly and accessible platform for soccer players to organize and participate in real-life games. With its intuitive interface, database integration, and community-focused features, the platform aims to enhance the soccer experience and make it easy for non-professional players to find like-minded peers. Thank you for considering my CS50 Final Project, Game Finder.




