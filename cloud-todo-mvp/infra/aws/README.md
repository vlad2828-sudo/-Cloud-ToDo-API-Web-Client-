# AWS deployment notes

This project is prepared for the following AWS target architecture:

```text
CloudFront
  ├─ S3 origin for static frontend
  └─ /api/* behavior to backend HTTPS origin

Backend container
  ├─ App Runner if available for the AWS account
  └─ ECS Fargate + ALB as fallback

Data
  ├─ RDS PostgreSQL in private subnets
  └─ Secrets Manager for DATABASE_URL and API_KEY

Observability
  └─ CloudWatch Logs
```

## Required secrets

Store backend runtime secrets in AWS Secrets Manager:

```text
DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname
API_KEY=generate-a-strong-value
```

Recommended API key generation:

```bash
openssl rand -hex 32
```

## App Runner deployment checklist

1. Push backend image to ECR.
2. Create App Runner service from ECR image.
3. Attach an instance role with permission to read required Secrets Manager secrets.
4. Add environment variables from Secrets Manager.
5. Configure VPC Connector for private RDS access.
6. Set port to `8000`.
7. Enable CloudWatch Logs.
8. Set CORS_ALLOWED_ORIGINS to your CloudFront domain.

## ECS Fargate fallback

Use this option if App Runner is unavailable for the AWS account:

1. Create ECS cluster.
2. Create task definition with backend image from ECR.
3. Configure Secrets Manager injection.
4. Place service in private subnets.
5. Attach Application Load Balancer in public subnets.
6. Configure HTTPS listener with ACM certificate.
7. Point CloudFront `/api/*` origin to the ALB domain.

## Frontend deployment checklist

1. Create private S3 bucket.
2. Create CloudFront distribution.
3. Use Origin Access Control for S3 access.
4. Upload `frontend/dist` to S3.
5. Set CloudFront error response fallback to `/index.html` for SPA routing.
6. Invalidate CloudFront cache after deploy.
