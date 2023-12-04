FROM node:16.13.1-alpine3.15

WORKDIR /app/frontend

COPY ./src /app/frontend/src
COPY ./public /app/frontend/public
COPY ./package.json /app/frontend/package.json
COPY ./postcss.config.js /app/frontend/postcss.config.js
COPY ./tailwind.config.js /app/frontend/tailwind.config.js
COPY ./index.html /app/frontend/index.html
COPY ./components.json /app/frontend/components.json
COPY ./jsconfig.json /app/frontend/jsconfig.json
RUN npm i