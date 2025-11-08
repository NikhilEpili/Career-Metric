# Build stage
FROM node:20-slim AS build

WORKDIR /app

# Copy package files and npm config
COPY package*.json .npmrc* ./

# Install dependencies using npm ci for deterministic builds
# Add small delay to avoid ETXTBSY error with esbuild
RUN npm ci || (sleep 2 && npm install)

COPY . .

RUN npm run build

# Runtime stage
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
