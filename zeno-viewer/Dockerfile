FROM node:24

WORKDIR /app

# Only copy what's needed to install dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Then copy the rest of the app
COPY . .

EXPOSE 5173

CMD ["yarn", "dev", "--host"]
