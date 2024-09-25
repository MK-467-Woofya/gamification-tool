# Installation and Setup
### Prerequisites
Ensure that you have the following installed:
- Node.js (v14 or later)
- npm (v6 or later)

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


### Backend Setup
1. In a terminal, navigate to the back_end directory:
- cd Interactive_map/back_end

2. Install Backend Dependencies
- npm install

3. Start the Backend Server
- npm start

4. The backend will be running on http://localhost:3000 and will store events in the events.json file.

### Frontend Setup (User Interactive Map)
1. Navigate to the Main Directory
- cd Interactive_map

2. Install Frontend Dependencies
- npm install

3. Additionally, install react-scripts and eslint-config-react-app for the frontend:
- npm install react-scripts --save
- npm install eslint-config-react-app --save-dev

4. If you face any npm errors, you can clean the npm cache:
- npm cache clean --force

### Build the Frontend
1. Build frontend 
- npm run build

2. Start the Frontend Server
- npm start
The frontend will be running on http://localhost:3001 (as http://localhost:3000 is used by the backend), allowing users to view events and check in.

### Common Errors
1. ESLint Configuration Error
- npm install eslint-config-react-app --save-dev
- npm cache clean --force
