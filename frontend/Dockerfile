# Dockerfile
# Stage 1: Build React app
FROM node:20-alpine as build
WORKDIR /app
COPY package.json .
RUN npm install
COPY src ./src
COPY public ./public
COPY index.html .
RUN npm run build

# Stage 2: Serve static files (e.g., using Nginx or simple static server)
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]