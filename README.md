# dalkeyhistoryforum

### Purpose of the website
This Dalkey History Forum web application comprises my project for Module 5: Frameworks of UCD's 24-03 Full-Stack Software Development Course. The objective of the project is as follows:

> Develop a web application that leverages the Django framework integrated with a PostgreSQL database. This integration aims to ensure efficient data management, from storing user messages to capturing intricate project details. By combining modern HTML, CSS powered by Bootstrap, and dynamic JavaScript functionalities, the end goal is to deliver a captivating user experience.

I chose to prepare a discussion forum web application on the history of Dalkey. The purpose of the project is to develop a web application that leverages the Django framework integrated with a PostgreSQL database to ensure efficient data management. The structure of the web application had regard to the following user stories:
- As a visitor, I want to browse the forum without logging in so that I can explore discussions before deciding to join.
- As a visitor, I want to register easily so that I can participate in discussions about Dalkey’s history.
- As a historian, I want to share my research findings so that I can contribute valuable knowledge to the forum.
- As a historian, I want to collaborate with other researchers on specific topics so that we can deepen our collective understanding of Dalkey’s past.
- As a local resident, I want to share stories passed down through generations so that others can learn about Dalkey’s oral history.
- As a local resident, I want to discuss historical landmarks and their significance so that I can raise awareness about Dalkey’s heritage.
- As a tourist, I want to ask questions about historical sites so that I can plan my visit to Dalkey.
- As a tourist, I want to share my experiences and photos of Dalkey’s historical landmarks so that others can learn from my visit.
- As a registered user, I want to create a new discussion thread so that I can share my knowledge and ask questions.
- As a registered user, I want to reply to posts so that I can engage with other history enthusiasts.
- As a registered user, I want to edit my posts so that I can correct mistakes or add more information.
- As a registered user, I want to upload photos so that I can share historical images.
- As a moderator, I want to delete or hide inappropriate posts so that the forum remains respectful and informative.
- As a moderator, I want to move threads to the correct category so that discussions stay organized.

*Please note*, however, that, due to the limited scope of the project, the Dalkey History Forum web application is not representative of all features that would need to be included in a discussion forum website. For example, having regard to the limited scope of the project, I decided not to allow ordinary users to delete their own profiles or to delete or edit threads due to cascading issues that would cause (although it is open to the user to delete the first post in a thread that they created). Users with admin privileges are, however, enabled to do that. Moreover, users are only enabled to upload one image per post. It is also noted that it would be desirable to have a function that would bring the user to the post they just made or updated, but that was a level of complexity that was considered outside the scope of this project.

### Required features of the website
The text below outlines the principal requirements of the project for the website and how each requirement was satisfied.

- *Application Structure.* The web application uses Django as the Backend Framework, PostreSQL for the database and HTML, CSS and JavaScript for the frontend.
- *Core Features.* As required, the web application includes the following core features: User Management; Registration and Login System; Allows users to update their personal and contact details; and Email-based recovery for forgotten passwords.
- *Data Storage.* The web application stores user information (username, email address, profile picture and password as well as autorisation status) and information on the discussion forum (topics, threads and posts, including which user created a thread or a post, when the thread or a post was created and the content of that thread or post). Users can update their own information in their user profile and can access a list of posts by user. Users can also update or delete their own posts.
- *User Interface.* The following design elements were used for the user interface: Bootstrap-driven responsive layouts ensuring compatibility across devices of varying screen sizes; HTML templates for consistent page structures, such as headers and footers; JavaScript-driven content that reacts to user inputs, such as real-time form validation. Please note that, in addition to the built-in Bootstrap JavaScript, the validation.js validates post content to prevent submission of any profane content using ProfanityAPI.
- *Security Features.* User roles and permissions were applied to restrict access to specific functionalities and data based on the user's role. The web application uses Django’s built-in data encryption methodologies to ensure sensitive data, especially user passwords, are stored securely.
- *Extension Capabilities.* The web application uses Django, which allows for future integrations like third-party APIs, additional database systems, or incorporating additional frontend frameworks. Please note that the third-party API, ProfanityAPI https://www.profanity.dev/, was used in the web application for form validation.

### Installation
A version of the website is deployed here: https://dalkeyhistoryforum.onrender.com/. To view this website off-line and/or make changes:
- clone the gitHub repository at https://github.com/amyhastings/dalkeyhistoryforum;
- pip install -r requirements.txt;
- go to https://cloudinary.com; generate a cloud name, API key and API secret key; and edit the .env file
- run all of the code blocks in the init_data.ipynb file;
- in the terminal, launch the application python ./app.py;
- to test the reset password functionality, generate a Google email application password and edit the corresponding fields in the .env file.

### Licensing
This web application is the copyright of Amy Hastings. The photographs for profile pictures were sourced from https://www.pexels.com. The default image used when the user has not uploaded their own profile picture was sourced from	https://www.freepik.com. Profanity checking of post inputs is undertaken using ProfanityAPI https://www.profanity.dev/.