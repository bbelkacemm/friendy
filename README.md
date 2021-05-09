# Chatbot for autistic children

## Introduction

## Prerequisites

You need to install first anaconda, npm and optionally docker

## How to use?

1. Create a conda environment using the file **environment.yml**

```shell
cd server
conda env create environment.yml
```

2. Prepare and launch database container

```shell
docker pull postgres
docker container run --name pfe -d -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres
```

3. Launch the server

```shell
# if you are on macos replace set with export
# use python.exe located on your environment's bin
set FLASK_DEBUG=0 && set FLASK_APP=server/app.py && python -m flask run
```

4. Launch the client (web)

```shell
cd client
npm run serve
```

## Features

### Server

- [x] Neural Network model
    - [x] Train
    - [x] Predict a context
- [x] Data initialization
    - [x] Users initialization
    - [x] Roles & permissions initialization
    - [x] Training data initialization

### Client (Web)

- [ ] Authentication
    - [x] Login
    - [x] Sign up (client)
    - [ ] Sign up demand (contributor)
- [ ] Dashboard
    - [x] Train model
    - [ ] Statistics
- [x] Chatbot
    - [x] Send a message
    - [x] Receive a response with its propositions
- [ ] Contributions
    - [x] Display contributions
    - [x] Add contribution
    - [ ] Edit contribution
    - [ ] Delete contribution
    - [ ] Validate contribution
- [ ] Users
    - [x] Display users
    - [x] Add user
    - [x] Edit user
    - [ ] Delete user
- [ ] Roles & Permissions
    - [x] Display roles/permissions
    - [x] Add role/permission
    - [x] Edit role/permission
    - [ ] Delete role/permission

### Client (mobile)

- [ ] Authentication
    - [ ] Login
    - [ ] Sign up
- [ ] Chatbot
    - [ ] Send a message
    - [ ] Receive a response with its propositions
