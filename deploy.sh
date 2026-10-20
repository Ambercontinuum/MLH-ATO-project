#!/bin/bash
set -e

# Configuration
REGISTRY="registry.digitalocean.com/civicpulse-registry"
APP_ID="b88c5a37-e445-4114-8f96-4ace58715b68"

echo "🚀 Starting deployment process..."

# Ensure we are logged in to the registry
echo "🔑 Checking registry authentication..."
doctl registry login

echo "📦 Building and pushing backend image..."
docker build -t $REGISTRY/backend:latest ./backend
docker push $REGISTRY/backend:latest

echo "📦 Building and pushing frontend image..."
docker build -t $REGISTRY/frontend:latest ./frontend
docker push $REGISTRY/frontend:latest

echo "☁️ Triggering DigitalOcean App update..."
# Use doctl to trigger a redeployment of the app
# This assumes the App Platform app is already configured to use these images
doctl apps create-deployment $APP_ID

echo "✅ Deployment triggered successfully!"
