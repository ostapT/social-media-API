## Social media API
This RESTful API allows users to create a profile, write, edit and delete their own posts. The functionality to follow other users to view their posts has also been implemented.


## Installation
```shell
git clone https://github.com/ostapT/social-media-API.git
cd social-media-API
python -m venv venv
source venv/bin/activate (on MacOS/Linux)
venv\Scripts\activate (on Windows)
pip install -r requirements.txt
````
Create .env file using .env.sample as a template.
Provide your info for variables inside it, for e.g. DJANGO_SECRET_KEY=your secret key
```shell
python manage.py migrate
python manage.py runserver
```

## Feauters

- JWT authentication 
- Create and retrieve user profile with detail information like bio etc.
- Implemented full CRUD for Post endpoint including image upload.
- Search functionality. Users can find another user by username or their post by title.
- The functionality to follow/unfollow other users to view their posts has also been implemented.
- Documentation is located on api/doc/swagger/