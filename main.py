
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import graphene
from schemas import PostSchema,PostModel,UserSchema
from models import Post,User
from db_conf import db_session
import bcrypt
from datetime import timedelta
from jwt_token import create_access_token,decode_access_token
from graphql import GraphQLError
from jwt import PyJWTError

db = db_session.session_factory()
app = FastAPI()

# Mutation to Authenticate the User if username & password matches with entry in DB
class AuthenticateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    ok = graphene.Boolean()
    token = graphene.String()

    @staticmethod
    def mutate(root,info,username,password):
        user = UserSchema(username=username,password=password)
        db_user_info = db.query(User).filter(User.username == username).first()
        if bcrypt.checkpw(user.password.encode("utf-8"), db_user_info.password.encode("utf-8")):
            access_token_expires = timedelta(minutes=60)
            access_token = create_access_token(data={"user":username},expires_delta=access_token_expires)
            ok = True
            return AuthenticateUser(ok=ok,token=access_token)
        else:
            ok = False
            return AuthenticateUser(ok=ok)

# Mutation to Create New User(Sign Up)
class CreateNewUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root,info,username,password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
        password_hash = hashed_password.decode("utf-8")
        user = UserSchema(username=username,password=password_hash)
        db_user = User(username=user.username,password=password_hash)
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            ok = True
            return CreateNewUser(ok)
        except:
            db.rollback()
            raise 
        db.close()

# Mutation to Create Post
class CreateNewPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        token = graphene.String(required=True)
    result = graphene.String()

    @staticmethod
    def mutate(root,info,title,content,token):
        try:
            payload = decode_access_token(data=token)
            username = payload.get("user")
            if username is None:
                raise GraphQLError("User is suspicious")
        except PyJWTError:
            raise GraphQLError("Invalid Token")

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise GraphQLError("User doesn't exist in DB")
        
        post = PostSchema(title=title,content=content)
        db_post = Post(title=post.title,content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        result = "Added New Post"
        return CreateNewPost(result=result)


# Query to get posts(by ID or allPosts)
class Query(graphene.ObjectType):
    all_posts = graphene.List(PostModel)
    post_by_id = graphene.Field(PostModel,post_id=graphene.Int(required=True))
    
    def resolve_all_posts(self,info):
        query = PostModel.get_query(info)
        return query.all()
    
    def resolve_post_by_id(self,info,post_id):
        return db.query(Post).filter(Post.id == post_id).first()

# Listing all mutations(Merging)
class PostMutations(graphene.ObjectType):
    authenticate_user = AuthenticateUser.Field()
    create_new_post = CreateNewPost.Field()
    create_new_user = CreateNewUser.Field()

# Defining the end point - Assigning Mutations & Query
app.add_route("/graphql",GraphQLApp(schema=graphene.Schema(mutation=PostMutations,query=Query)))
