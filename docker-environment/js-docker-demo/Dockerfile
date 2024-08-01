FROM node:20-alpine

WORKDIR /app

COPY testRunner.js .
COPY logger.js .
COPY main.js .

ENV NODE_ENV=production

CMD ["node", "main.js"]