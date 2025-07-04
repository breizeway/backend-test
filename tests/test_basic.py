import pytest
from app import create_app, db
from app.models import User, Post


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "backend-test"


def test_graphql_explorer(client):
    """Test GraphQL explorer endpoint"""
    response = client.get("/graphql")
    assert response.status_code == 200
    assert b"GraphQL" in response.data


def test_create_user_model(app):
    """Test User model creation"""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.created_at is not None

        # Test to_dict method
        user_dict = user.to_dict()
        assert user_dict["id"] == user.id
        assert user_dict["username"] == "testuser"
        assert user_dict["email"] == "test@example.com"


def test_create_post_model(app):
    """Test Post model creation"""
    with app.app_context():
        # Create user first
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        # Create post
        post = Post(title="Test Post", content="Test content", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        assert post.id is not None
        assert post.title == "Test Post"
        assert post.content == "Test content"
        assert post.user_id == user.id
        assert post.created_at is not None

        # Test relationship
        assert post.author == user
        assert post in user.posts


def test_graphql_users_query(client):
    """Test GraphQL users query"""
    query = """
    query {
        users {
            id
            username
            email
        }
    }
    """

    response = client.post(
        "/graphql", json={"query": query}, content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "users" in data["data"]
    assert isinstance(data["data"]["users"], list)


def test_graphql_create_user_mutation(client):
    """Test GraphQL create user mutation"""
    mutation = """
    mutation {
        createUser(username: "newuser", email: "new@example.com") {
            id
            username
            email
        }
    }
    """

    response = client.post(
        "/graphql", json={"query": mutation}, content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "createUser" in data["data"]

    user_data = data["data"]["createUser"]
    assert user_data["username"] == "newuser"
    assert user_data["email"] == "new@example.com"
    assert user_data["id"] is not None
