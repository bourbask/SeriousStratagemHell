# VanaStack

**VanaStack** is a modern Fullstack project using Node.js for the backend and React with TypeScript for the frontend. It implements tools like Bun, ESLint, Prettier, and Husky to ensure high code quality and efficient workflows. This project includes a concrete example of interconnection between the backend and frontend.

---

## Features

- **Backend with Node.js**:

  - Express server.
  - Endpoint `/api/message` returning a JSON message.
  - Complete TypeScript setup with Nodemon for automatic reloads.

- **Frontend with React and Vite**:

  - API call to the backend to display dynamic data.
  - TypeScript configuration with modern development tools.

- **Code Quality**:

  - Integration of ESLint, Prettier, and Husky for automatic linting before commits.

- **Modern Package Manager**:
  - Using Bun for improved performance and simplified dependency management.

---

## Prerequisites

Before starting, ensure you have:

1. **Bun**: [Install Bun](https://bun.sh/)
2. **Git**: [Download Git](https://git-scm.com/)
3. **Node.js (v18 or newer)**: [Download Node.js](https://nodejs.org/)
4. **Visual Studio Code**: [Download VS Code](https://code.visualstudio.com/)

---

## Installation

1. Clone the Git repository:

   ```bash
   git clone https://github.com/<your-username>/VanaStack.git
   cd VanaStack
   ```

2. Install backend dependencies and start the server:

   ```bash
   cd backend
   bun install
   bun run dev
   ```

3. Install frontend dependencies and start the UI:

   ```bash
   cd ../frontend
   bun install
   bun run dev
   ```

---

## Usage Example

- The backend exposes an endpoint at `http://localhost:5000/api/message` which returns:

  ```json
  { "message": "Hello from the backend!" }
  ```

- The frontend consumes this endpoint to display the message in the UI.

---

## Available Scripts

### Backend

- **`bun run dev`**: Starts the server with Nodemon.
- **`bun run start`**: Compiles and runs the backend.

### Frontend

- **`bun run dev`**: Starts the UI.
- **`bun run lint`**: Lints the code with ESLint.
- **`bun run lint:fix`**: Automatically fixes linting errors.

---

## Contribution

1. Fork the project.
2. Create a branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Add a new feature"
   ```

4. Push the branch to the remote repository:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
