# React-build & Nginx

# Stage 1: Build React App
FROM node:22-alpine as build
WORKDIR /app
COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install
COPY . .
RUN npm run build

# Stage 2: Setup Reverse Proxy nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf 
COPY --from=build /app/dist /usr/share/nginx/html