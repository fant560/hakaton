FROM node:11-alpine

COPY . .

RUN yarn install --ignore-engines

ENTRYPOINT ["yarn","start"]
