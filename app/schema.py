from ariadne import QueryType, MutationType
from .models import User, Post, db

# GraphQL Type Definitions
type_defs = """
    type User {
        id: ID!
        username: String!
        email: String!
        createdAt: String!
        updatedAt: String!
        posts: [Post!]!
    }
    
    type Post {
        id: ID!
        title: String!
        content: String!
        userId: ID!
        author: User!
        createdAt: String!
        updatedAt: String!
    }
    
    type Query {
        users: [User!]!
        user(id: ID!): User
        posts: [Post!]!
        post(id: ID!): Post
    }
    
    type Mutation {
        createUser(username: String!, email: String!): User!
        createPost(title: String!, content: String!, userId: ID!): Post!
        updateUser(id: ID!, username: String, email: String): User!
        updatePost(id: ID!, title: String, content: String): Post!
        deleteUser(id: ID!): Boolean!
        deletePost(id: ID!): Boolean!
    }
"""

# Query resolvers
query = QueryType()


@query.field("users")
def resolve_users(_, info):
    print("Fetching all users")
    users = User.query.all()
    return [user.to_dict() for user in users]


@query.field("user")
def resolve_user(_, info, id):
    print(f"Fetching user with id: {id}")
    user = User.query.get(id)
    return user.to_dict() if user else None


@query.field("posts")
def resolve_posts(_, info):
    print("Fetching all posts")
    posts = Post.query.all()
    return [post.to_dict() for post in posts]


@query.field("post")
def resolve_post(_, info, id):
    print(f"Fetching post with id: {id}")
    post = Post.query.get(id)
    return post.to_dict() if post else None


# Mutation resolvers
mutation = MutationType()


@mutation.field("createUser")
def resolve_create_user(_, info, username, email):
    print(f"Creating user: {username}, {email}")
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


@mutation.field("createPost")
def resolve_create_post(_, info, title, content, userId):
    print(f"Creating post: {title} for user {userId}")
    post = Post(title=title, content=content, user_id=userId)
    db.session.add(post)
    db.session.commit()
    return post.to_dict()


@mutation.field("updateUser")
def resolve_update_user(_, info, id, username=None, email=None):
    print(f"Updating user {id}")
    user = User.query.get(id)
    if not user:
        return None

    if username:
        user.username = username
    if email:
        user.email = email

    db.session.commit()
    return user.to_dict()


@mutation.field("updatePost")
def resolve_update_post(_, info, id, title=None, content=None):
    print(f"Updating post {id}")
    post = Post.query.get(id)
    if not post:
        return None

    if title:
        post.title = title
    if content:
        post.content = content

    db.session.commit()
    return post.to_dict()


@mutation.field("deleteUser")
def resolve_delete_user(_, info, id):
    print(f"Deleting user {id}")
    user = User.query.get(id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True


@mutation.field("deletePost")
def resolve_delete_post(_, info, id):
    print(f"Deleting post {id}")
    post = Post.query.get(id)
    if not post:
        return False

    db.session.delete(post)
    db.session.commit()
    return True


# Export resolvers
resolvers = [query, mutation]
