# Backend Test

A Python backend server built with Flask, GraphQL, SQLAlchemy, and Ariadne, designed for AWS deployment.

## Features

- **Flask**: Web framework for Python
- **GraphQL**: Query language with Ariadne
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Production database
- **AWS Infrastructure**: CloudFormation, ECS, RDS, ALB
- **Docker**: Containerized application
- **Flask-Migrate**: Database migrations
- **CORS**: Cross-origin resource sharing

## Project Structure

```
backend-test/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models.py            # SQLAlchemy models
│   └── schema.py            # GraphQL schema and resolvers
├── aws/
│   └── cloudformation.yaml  # AWS infrastructure template
├── scripts/
│   ├── setup.sh            # Development setup script
│   └── deploy-aws.sh       # AWS deployment script
├── app.py                   # Application entry point
├── config.py               # Configuration classes
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Local development setup
└── env.example           # Environment variables template
```

## Quick Start

### Option 1: Local Development (Recommended)

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd backend-test
   ./scripts/setup.sh
   ```

2. **Run the application:**

   ```bash
   source venv/bin/activate
   python app.py
   ```

3. **Access the application:**
   - GraphQL Explorer: http://localhost:5000/graphql
   - Health Check: http://localhost:5000/health

### Option 2: Docker Development

1. **Run with Docker Compose:**

   ```bash
   docker-compose up
   ```

2. **Access services:**
   - Application: http://localhost:5000/graphql
   - Database Admin: http://localhost:8080 (Adminer)

## GraphQL API

### Example Queries

**Get all users:**

```graphql
query {
  users {
    id
    username
    email
    createdAt
  }
}
```

**Create a user:**

```graphql
mutation {
  createUser(username: "john_doe", email: "john@example.com") {
    id
    username
    email
    createdAt
  }
}
```

**Get user with posts:**

```graphql
query {
  user(id: "1") {
    id
    username
    email
    posts {
      id
      title
      content
      createdAt
    }
  }
}
```

**Create a post:**

```graphql
mutation {
  createPost(
    title: "Hello World"
    content: "This is my first post"
    userId: "1"
  ) {
    id
    title
    content
    author {
      username
    }
    createdAt
  }
}
```

## Database Models

### User Model

- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `posts`: Relationship to posts

### Post Model

- `id`: Primary key
- `title`: Post title
- `content`: Post content
- `user_id`: Foreign key to user
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `author`: Relationship to user

## Environment Configuration

Create a `.env` file (copy from `env.example`):

```bash
FLASK_CONFIG=development
FLASK_ENV=development
SECRET_KEY=your-secret-key
PORT=5000

# Database
DATABASE_URL=sqlite:///backend_test.db
DEV_DATABASE_URL=sqlite:///backend_test_dev.db

# AWS (for production)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

## AWS Deployment

### Prerequisites

- AWS CLI installed and configured
- Docker installed
- AWS account with appropriate permissions

### Deploy Infrastructure

1. **Deploy AWS resources:**

   ```bash
   ./scripts/deploy-aws.sh production us-east-1
   ```

2. **Build and push Docker image:**

   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name backend-test --region us-east-1

   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Build and push image
   docker build -t backend-test .
   docker tag backend-test:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/backend-test:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/backend-test:latest
   ```

### AWS Resources Created

- **VPC**: Virtual Private Cloud with public/private subnets
- **RDS**: PostgreSQL database in private subnets
- **ECS**: Container orchestration service
- **ALB**: Application Load Balancer
- **Security Groups**: Network security rules
- **IAM Roles**: Service permissions

## Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Database migrations
flask db init
flask db migrate -m "Description"
flask db upgrade

# Run tests
pytest

# Docker commands
docker-compose up          # Start all services
docker-compose down        # Stop all services
docker-compose logs        # View logs
```

## API Endpoints

- `GET /graphql` - GraphQL Explorer interface
- `POST /graphql` - GraphQL API endpoint
- `GET /health` - Health check endpoint

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py
```

## Configuration

The application supports multiple environments:

- **Development**: SQLite database, debug mode
- **Production**: PostgreSQL database, optimized settings
- **Testing**: In-memory SQLite, testing configurations

## Security Features

- Environment-based configuration
- Database connection pooling
- CORS protection
- Input validation
- SQL injection prevention via SQLAlchemy

## Monitoring & Logging

- Health check endpoint for load balancer
- Application logging to stdout
- Database connection monitoring
- GraphQL query logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Write tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
