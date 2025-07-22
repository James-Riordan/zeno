# Stage 1: Build
FROM node:24 AS builder

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
RUN yarn build

# Stage 2: Run the SvelteKit Node server
FROM node:24 AS runner

WORKDIR /app

# Copy only what's needed to run the SvelteKit server
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.svelte-kit ./svelte-kit
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["node", "build"]
