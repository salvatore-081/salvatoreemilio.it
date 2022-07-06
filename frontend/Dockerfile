FROM node:alpine as node
WORKDIR /app
COPY . .
RUN npm install --force
RUN npm run build salvatoreemilio.it --configuration=production

FROM nginx:alpine
COPY --from=node /app/dist/apps/salvatoreemilio.it /usr/share/nginx/html
