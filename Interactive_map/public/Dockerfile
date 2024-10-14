# Base image for frontend
FROM node:20-alpine

# Set work directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package.json /usr/src/app/
RUN npm install

# Copy the rest of the source code
COPY . /usr/src/app

# Expose port 3001 for the frontend
EXPOSE 3001

# Start the frontend server on port 3001
CMD ["npm", "start"]
