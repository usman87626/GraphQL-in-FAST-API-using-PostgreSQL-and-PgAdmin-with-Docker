
# Applying Alembic Migrations when set
alembic init alembic
docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head

# Queries
query {
    allPosts{
        title
    }
}

query{
    postById(postId:2){
        id
        title
        content
    }
}


mutation CreateNewUser{
    createNewUser(username:"lastuser",password:"last-user"){
        ok
    }
}

mutation authenticateUser{
  authenticateUser(username:"lastuser",password:"last-user"){
    ok
    token
  }
}

mutation CreateNewPost{
    createNewPost(title:"last-one",content:"hehehe",token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibGFzdHVzZXIiLCJleHAiOjE2MzE5OTI4Mzh9.G_f5ruMsi2v6sbidOm3jrL1pN5kzz7DRBQE3PhPL06o"){
        result
    }
}