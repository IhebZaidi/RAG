# Étape 1 : Construire l'application Angular
FROM node:18 as build
WORKDIR /app
COPY package.json ./ 
RUN npm install
COPY . . 
RUN npm run build --prod

# Étape 2 : Servir avec Nginx
FROM nginx:alpine
COPY --from=build /app/dist/rag-frontend/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
