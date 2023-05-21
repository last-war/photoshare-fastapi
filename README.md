# Photoshare-fastapi

Command project from python web 9 stream GoIT

## Technologies
* Python (Fastapi, SQLAlchemy, jose, alembic) )
* Cloudinary \ QRcode
* Pytest \ Unitest
* PostgreSQL

# Instruction
  
## How to install?
* clone repository [https://github.com/last-war/photoshare-fastapi](repository)
* you need environment variables:
DATABASE_URL=postgresql://postgres:secret@{your_DBadress}:{your_DBport}/{DB_name}
POSTGRES_DB={postgres_db_name}
POSTGRES_USER={postgres_user}
POSTGRES_PASSWORD={secret_db_key}
SECRET_KEY={secret_key_for_hash}
ALGORITHM=HS256
CLOUDINARY_NAME={your_cloudinary_name}
CLOUDINARY_API_KEY={your_cloudinary_api_key}
CLOUDINARY_API_SECRET={your_cloudinary_api_secret}
* don't forget do empty DB and execute: "alembic upgrade head" 
* simple way just run main.py: uvicorn.run(app, host="127.0.0.1", port=8000)
* 

## How to use?
### Authorization

* Sign up page at the api/auth/signup page. For 1st user need admin access.
* After your succesfull sign up, admin can change your access or you can use app as user.

### Features

* Upload your own photos.
* Search all you photos.
* Transform your posted pictures.
* Add up to 5 tags for each image.
* Create comments under posts.
* Search photos by tags.
* Rate posts.
* Admin and Moderator functions
* To see other capabilites, check [documentation](link).

## Our Team:
Developer: [Olga Pasichnyuk](https://github.com/olgapasichnyuk)  
Developer: [Oleh Ovchinnikov](https://github.com/xoka-pro)  
Developer: [Oleksii Kukhariev](https://github.com/flatline-code)  
Scrum Muster/Developer: [Vladislav Tymoshchuk](https://github.com/TimVladislav13010)  
Team Lead/Developer: [Andriy Maibrodskiy](https://github.com/last-war)
