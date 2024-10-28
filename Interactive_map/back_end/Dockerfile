# Use an official Node.js runtime as a base image
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json files to the container
COPY package.json package-lock.json /usr/src/app/

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . /usr/src/app

# Expose port 3002 (or the port your backend uses)
EXPOSE 3002

# Start the server (assuming your entry point is server.js)
CMD ["node", "server.js"]
