# Installation and Setup
### Prerequisites
Ensure that you have the following installed:
- Node.js (v14 or later)
- npm (v6 or later)

### Making config.js file
1. Make a config.js file in the public js folder
2. Copy and paste the below into the config.js file, and change the API key to your API key
const CONFIG = {
    BASE_URL: 'http://localhost:3002/',
    API_KEY: 'Your API key'
};


### Installing Node.js and npm
If you don’t have Node.js and npm installed, follow these instructions:
1. Update the package list:
- sudo apt update

2. Install Node.js:
- sudo apt update

3. Verify the installation:
- node -v

4. Install npm (if it’s not bundled with Node.js):
- sudo apt install npm

### Starting the program
1. In a terminal, navigate to the back_end directory:
- cd Interactive_map/back_end

2. Install Backend Dependencies
- npm install

3. Start the Backend Server
- npm start

4. The backend will be running on http://localhost:3002

### Backend Api 
1. Run backend for locations
docker-compose exec api python manage.py makemigrations locations
docker-compose exec api python manage.py migrate locations
