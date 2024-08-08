Authentication App 


The user first enters his mobile number.
If the user has already registered, he will be authenticated by entering the password.
Otherwise, a one-time 6-digit code will be generated for the user, which will be sent to him via SMS.
By entering the code, the user is registered and then personal information such as first and last name  is taken from him.
In the login process, if the user enters the wrong username three times or the wrong combination of username and password is entered three times from the same IP address, it will be blocked for 1 hour.
 In the same way, in the registration process, if three SMS requests come from the same IP but the entered code is wrong, or a number enters the wrong code three times, it will be blocked for 1 hour.(prevent of brute force)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [TEST SCREEN](#test_screen)

## Features

- Create, update, delete, and list tasks and projects
- Add comments to tasks
- Real-time notifications using Django Channels
- Background tasks with Celery and RabbitMQ
- Cache with redis
- API documentation with Swagger

## Requirements

- Docker
- Docker Compose

## Installation

1. **Clone the repository:**

   ```sh
   git clone git@github.com:arezoo88/authentication_app.git
   cd source
   ```

2. **Build and start the Docker containers:**

   ```sh
   docker-compose up --build
   ```


## Running the Project

1. **Start Server:**

   ```sh
   python manage.py runserver
   ```