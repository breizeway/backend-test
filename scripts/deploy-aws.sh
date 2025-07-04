#!/bin/bash

# AWS Deployment Script for Backend Test
set -e

# Configuration
ENVIRONMENT=${1:-development}
REGION=${2:-us-east-1}
STACK_NAME="backend-test-${ENVIRONMENT}"
DB_PASSWORD=${DB_PASSWORD:-$(openssl rand -base64 32)}

echo "Deploying Backend Test to AWS..."
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Stack Name: $STACK_NAME"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install AWS CLI."
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "AWS credentials are not configured. Please run 'aws configure'."
    exit 1
fi

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file aws/cloudformation.yaml \
    --stack-name "$STACK_NAME" \
    --parameter-overrides \
        Environment="$ENVIRONMENT" \
        DBPassword="$DB_PASSWORD" \
    --capabilities CAPABILITY_IAM \
    --region "$REGION"

# Get stack outputs
echo "Getting stack outputs..."
VPC_ID=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`VPCId`].OutputValue' \
    --output text \
    --region "$REGION")

DB_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
    --output text \
    --region "$REGION")

ALB_DNS=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
    --output text \
    --region "$REGION")

ECS_CLUSTER=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`ECSClusterName`].OutputValue' \
    --output text \
    --region "$REGION")

echo "Infrastructure deployed successfully!"
echo ""
echo "Stack Outputs:"
echo "VPC ID: $VPC_ID"
echo "Database Endpoint: $DB_ENDPOINT"
echo "Load Balancer DNS: $ALB_DNS"
echo "ECS Cluster: $ECS_CLUSTER"
echo ""
echo "Database Password: $DB_PASSWORD"
echo "Please save the database password securely!"
echo ""
echo "Next steps:"
echo "1. Build and push Docker image to ECR"
echo "2. Create ECS task definition"
echo "3. Create ECS service"
echo "4. Configure domain name (optional)"
echo ""
echo "Application will be available at: http://$ALB_DNS" 