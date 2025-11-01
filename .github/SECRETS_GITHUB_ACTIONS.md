# Eagle Eye GitHub Actions Secrets Reference

## Overview

This file documents how to set up GitHub Secrets for CI/CD pipelines.

## GitHub Secrets Setup

### Step 1: Go to Repository Settings

```
Settings → Secrets and variables → Actions → New repository secret
```

### Step 2: Add Each Secret

Add the following secrets (values should match your production/staging environment):

| Secret Name | Value | Example |
|------------|-------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |
| `DATABASE_URL` | Production database connection | `postgresql+psycopg://...` |
| `S3_ACCESS_KEY` | Production S3 access key | `AKIA...` |
| `S3_SECRET_KEY` | Production S3 secret key | `...` |
| `S3_ENDPOINT` | Production S3 endpoint | `https://s3.amazonaws.com` |
| `REDIS_URL` | Production Redis URL | `redis://prod-redis:6379` |
| `N8N_API_KEY` | n8n API key | `n_...` |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | `xxxxxxxx-xxxx-...` |
| `AZURE_TENANT_ID` | Azure tenant ID | `xxxxxxxx-xxxx-...` |
| `REGISTRY_USERNAME` | Docker registry username | `myregistry` |
| `REGISTRY_PASSWORD` | Docker registry password | `...` |

## GitHub Workflow Example

```yaml
# .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Build and Deploy API
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          S3_ACCESS_KEY: ${{ secrets.S3_ACCESS_KEY }}
          S3_SECRET_KEY: ${{ secrets.S3_SECRET_KEY }}
          S3_ENDPOINT: ${{ secrets.S3_ENDPOINT }}
          REDIS_URL: ${{ secrets.REDIS_URL }}
          ENVIRONMENT: production
        run: |
          cd services/api
          pip install -r requirements.txt
          python -m pytest
          # Deploy steps here
      
      - name: Build Docker Image
        env:
          REGISTRY: myregistry.azurecr.io
          IMAGE_TAG: latest
        run: |
          echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login -u "${{ secrets.REGISTRY_USERNAME }}" --password-stdin ${{ env.REGISTRY }}
          docker build -t ${{ env.REGISTRY }}/api:${{ env.IMAGE_TAG }} .
          docker push ${{ env.REGISTRY }}/api:${{ env.IMAGE_TAG }}
```

## Environment Variables vs Secrets

### Use GitHub Secrets For:
- API keys (OpenAI, etc.)
- Database passwords
- Cloud provider credentials
- Registry credentials
- Private tokens (n8n, etc.)

### Use Environment Variables For:
- Public configuration (host, port, endpoint URLs without credentials)
- Feature flags
- Log levels
- Non-sensitive settings

```yaml
env:
  LOG_LEVEL: INFO
  API_PORT: 8000
  S3_ENDPOINT: ${{ secrets.S3_ENDPOINT }}  # Mix both
```

## Organization Secrets

For sharing secrets across multiple repositories:

```
Settings → Secrets and variables → Actions → Organization secrets
```

Then reference in workflows:
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Rotating Secrets

### When to Rotate
- Every 90 days (best practice)
- If accidentally exposed
- After personnel changes
- After security incident

### How to Rotate

1. **Create new secret in GitHub:**
   ```
   Settings → Secrets → Update secret
   ```

2. **Update all services to use new value:**
   - Re-deploy with new secret
   - Monitor logs for successful connection

3. **Revoke old secret:**
   - OpenAI: Delete old key from https://platform.openai.com/api-keys
   - Database: Change password in cloud provider
   - AWS/Azure: Deactivate old access key

4. **Verify old secret isn't in use:**
   ```bash
   grep -r "old_key" .github/
   ```

## Testing Secrets Locally

### Don't commit real secrets!

Instead, use `.env.local`:
```bash
# Create from template
cp .env.example .env.local

# Add real values (local only)
# This file is git-ignored
```

### Simulate GitHub Actions locally

```bash
# Using act - https://github.com/nektos/act
act --secret-file .env.local
```

## Troubleshooting

### Secret not available in workflow

**Problem:**
```
Error: Secrets are not available for pull requests from forks
```

**Solution:**
```yaml
# In your workflow:
if: github.event_name != 'pull_request_target' || github.event.pull_request.head.repo.full_name == github.repository
```

### Secret value is masked in logs

**Expected behavior:**
```
*** (the secret value is masked)
```

**Don't try to unmask:**
```yaml
# WRONG - don't do this:
echo "${{ secrets.OPENAI_API_KEY }}"  # Output: ***
```

### Updating a secret doesn't take effect

**Solution:**
1. Go to Settings → Secrets → Delete secret
2. Add it again with new value
3. Re-run workflow

## Security Best Practices

✅ DO:
- Rotate secrets every 90 days
- Use unique secrets per environment (prod, staging, dev)
- Review organization secret access regularly
- Audit GitHub Actions usage
- Use branch protection rules

❌ DON'T:
- Print secrets in logs
- Commit secrets to repository
- Share secrets outside GitHub
- Use same secret across environments
- Store secrets in documentation

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Secret scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OpenAI API Key Security](https://platform.openai.com/docs/guides/production-best-practices/api-key-security)
