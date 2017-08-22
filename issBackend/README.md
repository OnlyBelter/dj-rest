## About
This is the backend of [Image sharing system](https://github.com/OnlyBelter/image-sharing-system)

## User
I created 13 users that contain 1 super user(admin) and 12 normal users.
All of them have same password: password123
- admin: belter
- normal user: xiongx, Jim, Mr._Nice, Narco, Bombasto, Celeritas, 
               Magneta, RubberMan, Dynama, Dr_IQ, Magma, Tornado
               
## Url(endpoint)
Start this project by dj-rest\issBackend>python manage.py runserver 0.0.0.0:8000
- Api Root: http://localhost:8000/

- User List(only admit can access): http://localhost:8000/users/  
- User Instance: http://localhost:8000/users/1/

- Image List: http://localhost:8000/images/
- Image Instance: http://localhost:8000/images/1/
