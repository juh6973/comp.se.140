FROM node:24-slim
WORKDIR /app
COPY package.json package-lock.json* ./

RUN npm install --omit=dev
COPY tsconfig.json ./
COPY src ./src
RUN npx tsc
EXPOSE 3000
CMD ["node", "dist/index.js"]