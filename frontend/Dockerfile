# Choose the Image which has Node installed already

FROM node:14.18-alpine

# make the "app" folder the current working directory
RUN mkdir -p /frontend
WORKDIR /frontend

RUN apk update && apk upgrade
RUN apk add git

# copy both "package.json" and "package-lock.json" (if available)
COPY package*.json ./

COPY . .

# install project dependencies
RUN npm install


ENV NUXT_HOST=0.0.0.0
# set app port
ENV NUXT_PORT=8081

CMD [ "npm","run","dev" ]

