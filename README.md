# GraphQL with Fast API using Dockerized Postgre DB & Pg-Admin
Use the following guidelines to run the project
## Pre-requisite:
- Docker

# How to Run

## Docker Compose
1. Open terminal in the project directory.
2. Type `docker-compose build` and wait for it to complete
3. Type `docker-compose up` and wait for it.
4. Now you can use the app on `127.0.0.1:8000/graphql`
5. Similarly, you can see the admin dashboard on `http://localhost:5050/`

All the credentials for DB are in `.env` file, you can edit it as well but do it wisely.
NOTE: "Never Upload `.env` or `.env.local` on Github or public repos. I uploaded it so that you can learn. 

## Database Migrations
You can migrate database as well after running the container using the above steps, steps for migrations are:
1. Type `docker-compose run app alembic revision --autogenerate -m "YOUR_MESSAGE_HERE"`
2. Then simply use the command `docker-compose run app alembic upgrade head` to save the changes.


# Queries
You can use the following Queries to add or fetch data from Database:

## Query to get All the Posts from Database
<pre>
query {
    allPosts{
        title
    }
}
</pre>

## Query to get Posts By ID:
<pre>
query{
    postById(postId:2){
        id
        title
        content
    }
}
</pre>

## Query to Create a New User

<pre>
mutation CreateNewUser{
    createNewUser(username:"NAME_OF_USER",password:"PASSWORD_OF_USER"){
        ok
    }
}
</pre>

## Query to authenticate the User usign JSON Web Token(JWT) Authentication
<pre>
mutation authenticateUser{
  authenticateUser(username:"lastuser",password:"last-user"){
    ok
    token
  }
}
</pre>

## Query to Create a New Post
<pre>
mutation CreateNewPost{
    createNewPost(
                title:"TITLE_OF_THE_POST",
                content:"CONTENT_OF_THE_POST",
                token:"JWT_TOKEN_ACQUIRED_AFTER_AUTHENTICATING_THE_USER"){
        result
    }
}
</pre>
