<br /><br />

<p align="center">
<a href="https://devleague.io">
  <img src="https://devleague.io/logo.png" alt="DevLeague Logo" width="70">
</a>
</p>
<h1 align="center"><b>DevLeague</b></h1>
<p align="center"><b>Your Github profile as a Pokemon card</b></p>


Welcome to the backend repository of [DevLeague.io](https://devleague.io), built using [FastAPI](https://fastapi.tiangolo.com/), a modern Python framework that is easy to learn and use.

For the frontend, see [devleague-client](https://github.com/ssaini4/devleague-client).

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project serves as the backend for DevLeague.io.

## Getting Started

To set up the project locally, follow the steps below.

### Prerequisites

Ensure you have the following installed:

- [Python](https://www.python.org/) (version 3.10 or later)
- [Docker](https://www.docker.com/) (to avoid OS-level dependency issues)
- [Visual Studio Code](https://code.visualstudio.com/) (the preferred editor for development)
- [Cursor](https://www.cursor.com/) (the preferred IDE for development)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ssaini4/devleague-backend.git
   cd devleague-backend
   ```

2. **Install Dependencies:**
   1. Open the Command Palette in VSCode (F1 or Ctrl+Shift+P)
   2. Search for and select "Remote-Containers: Reopen in Container"
   3. VSCode will restart and build the development container
   4. Once initialization completes (this may take a few minutes), you'll be working inside the containerized environment with all dependencies installed

   The container provides an isolated development environment with all required dependencies pre-configured.

3. **Create a .env file:**

   Copy the .env.example file and rename it to .env.
   Fill in the values for the environment variables.


### Running the Application in VSCode development container

To start the development server:

```bash
./run_dev.sh
```

By default, the application will be accessible at `http://localhost:8080`. 

### Built using
[![FastAPI](https://img.shields.io/pypi/v/pypi.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/pypi/v/sqlalchemy.svg?logo=sqlalchemy)](https://www.sqlalchemy.org/)

## Contributing

We welcome contributions! Please create a new issue with your idea or feature request.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.