# **Backend Service Design Document**

This design document provides a detailed overview of the backend service
architecture for the personal assistant application. The integration of
LangChain components—agents, chains, and tools—is encapsulated within the `core`
package, clarifying their roles and interactions. By structuring the code in
this way, we ensure that reusable components are easily accessible and
maintainable.

The inclusion of boilerplate code offers a practical starting point for
developers, highlighting how different modules interact and how key technologies
are implemented. The appendix serves as a helpful resource for novice readers,
explaining essential concepts like CORS, sessions, and authentication, and
demonstrating how FastAPI facilitates these functionalities.

By adhering to the architectural guidelines and guardrails, this design promotes
a modular, scalable, and maintainable backend service that leverages open-source
technologies and aligns with industry best practices.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Architectural Overview](#architectural-overview)
3. [Functional Decomposition](#functional-decomposition)
   - [Modules and Responsibilities](#modules-and-responsibilities)
   - [Interfaces and Interactions](#interfaces-and-interactions)
4. [Key Design Decisions and Rationale](#key-design-decisions-and-rationale)
5. [Key Design Patterns](#key-design-patterns)
6. [Key Technologies and Considerations](#key-technologies-and-considerations)
7. [Execution Architecture](#execution-architecture)
   - [Synchronous vs. Asynchronous
     Communication](#synchronous-vs-asynchronous-communication)
   - [Background Processing](#background-processing)
8. [Project Code Outline](#project-code-outline)
   - [Module Enumeration and
     Functionality](#module-enumeration-and-functionality)
9. [Module Design Details and Boilerplate
   Implementations](#module-design-details-and-boilerplate-implementations)
   - [1. `main.py` (Entry Point)](#1-mainpy-entry-point)
   - [2. `api` Package](#2-api-package)
   - [3. `services` Package](#3-services-package)
   - [4. `core` Package](#4-core-package)
     - [4.1 `agents` Module](#41-agents-module)
     - [4.2 `chains` Module](#42-chains-module)
     - [4.3 `tools` Module](#43-tools-module)
   - [5. `models` Package](#5-models-package)
   - [6. `database` Package](#6-database-package)
   - [7. `config.py` (Configuration)](#7-configpy-configuration)
   - [8. `utils` Package](#8-utils-package)
10. [Appendix](#appendix)
    - [A. Background on CORS Middleware, Sessions, and
      Authentication](#a-background-on-cors-middleware-sessions-and-authentication)

---

## **Overview**

The backend service is the core component of the personal assistant web
application. It is responsible for:

- **Providing the Frontend API**: Exposing endpoints for the frontend to
  interact with.
- **Hosting App-Specific Business Logic**: Implementing the core functionalities
  required by the application.
- **Incorporating the LangChain Framework**: Facilitating interactions with
  Large Language Models (LLMs), managing chains, agents, and tools.
- **Utilizing Reusable Agent Definitions**: Integrating agents based on
  app-specific needs while leveraging reusable components.
- **Connecting to the Ollama-Hosted LLM**: Communicating with locally hosted
  LLMs via Ollama.
- **Processing Input and Requests**: Handling requests from the frontend, which
  may involve LLM calls, agent triggers, or non-LLM processing.

---

## **Architectural Overview**

The backend service follows a **modular layered architecture** designed for
scalability, maintainability, and reusability. The layers are:

1. **API Layer**: Handles HTTP requests and responses.
2. **Service Layer**: Contains business logic and orchestrates interactions
   between components.
3. **Core Layer**: Manages LangChain integration, including agents, chains, and
   tools.
4. **Data Access Layer**: Interfaces with the database and external data
   sources.
5. **Utility Layer**: Provides shared utilities and helper functions.

---

## **Functional Decomposition**

### **Modules and Responsibilities**

1. **API Layer (`api` package)**
   - Expose RESTful endpoints to the frontend.
   - Handle request validation and response formatting.
   - Manage authentication and authorization.

2. **Service Layer (`services` package)**
   - Implement app-specific business logic.
   - Coordinate between the API layer, core layer, and data access layer.
   - Handle non-LLM processing tasks.

3. **Core Layer (`core` package)**
   - **`agents` Module**
     - Define reusable and app-specific agents using LangChain.
   - **`chains` Module**
     - Define LangChain chains that represent sequences of operations.
   - **`tools` Module**
     - Implement reusable tools that agents can use.
     - Tools can access data sources or external APIs.

4. **Data Access Layer (`database` and `models` packages)**
   - Define database models using SQLAlchemy.
   - Provide data access methods for CRUD operations.
   - Manage connections to databases and external APIs.

5. **Utility Layer (`utils` package)**
   - Offer utility functions and helpers (e.g., logging, error handling).
   - Manage configurations and environment variables.

### **Interfaces and Interactions**

- **API Layer ↔ Service Layer**: API calls service methods to process requests.
- **Service Layer ↔ Core Layer**: Services invoke agents or chains for
  LLM-related tasks.
- **Core Layer ↔ Ollama LLM**: Agents and chains communicate with the LLM
  through Ollama's API.
- **Core Layer ↔ Data Access Layer**: Tools within the core layer access data
  via the data access layer.
- **Service Layer ↔ Data Access Layer**: Services perform data operations via
  data access methods.
- **Utility Layer**: Accessible by all layers for shared functionalities.

---

## **Key Design Decisions and Rationale**

1. **Module Naming and Organization**
   - *Rationale*: To better reflect the components of LangChain (chains, agents,
     tools), the `agents` package is renamed to `core`.
   - *Decision*: Create a `core` package containing `agents`, `chains`, and
     `tools` modules.

2. **LangChain Integration**
   - *Rationale*: LangChain structures applications into chains, agents, and
     tools.
   - *Decision*: Implement these components within the `core` package to
     encapsulate LangChain integration.

3. **Reusable Tools**
   - *Rationale*: Tools are reusable components that can be used by multiple
     agents.
   - *Decision*: Implement tools as independent modules within the `tools`
     module, facilitating reuse and modularity.

4. **Data Access in Tools**
   - *Rationale*: Tools may need to access databases or external APIs.
   - *Decision*: Tools will interact with the data access layer to retrieve or
     store data.

5. **Asynchronous Operations**
   - *Rationale*: Enhance performance, especially when dealing with I/O-bound
     operations like LLM calls or API requests.
   - *Decision*: Use asynchronous programming throughout the backend where
     appropriate.

---

## **Key Design Patterns**

1. **Factory Pattern** (For Agent and Tool Creation)
   - Enables dynamic creation of agents and tools based on configuration or
     runtime parameters.

2. **Dependency Injection**
   - Facilitates testing and promotes loose coupling between components.

3. **Repository Pattern** (In Data Access Layer)
   - Abstracts data access logic and provides a clean separation between the
     service layer and data storage.

4. **Asynchronous Programming**
   - Improves scalability by non-blocking I/O operations.

---

## **Key Technologies and Considerations**

- **Python 3.9+**
  - Utilize modern language features and typing enhancements.

- **FastAPI**
  - Attention Points:
    - Proper use of async/await.
    - Middleware for CORS, authentication, and sessions.
    - See [Appendix
      A](#a-background-on-cors-middleware-sessions-and-authentication) for more
      details.

- **LangChain**
  - Typical Use:
    - Define chains, agents, and tools for LLM interactions.
    - Manage conversation state and memory.

- **Ollama**
  - Considerations:
    - Ensure the Docker container is accessible to the backend.
    - Manage model loading and resource utilization.

- **SQLAlchemy**
  - Attention Points:
    - Session management.
    - Asynchronous support using `asyncpg` for PostgreSQL.

- **Docker and Docker Compose**
  - Use for containerizing the application and orchestrating services.

---

## **Execution Architecture**

### **Synchronous vs. Asynchronous Communication**

- **Synchronous Communication**
  - Used within the same process where operations are quick and non-blocking.
  - Example: Data validation, in-memory computations.

- **Asynchronous Communication**
  - Used for I/O-bound operations that may block the thread.
  - Example: Network calls to the LLM via Ollama, database queries, external API
    calls via tools.

### **Background Processing**

- **Async/Await**
  - Use Python's `asyncio` library to write asynchronous code.
  - FastAPI endpoints should be defined with `async def` to support async
    operations.

- **Threading**
  - For CPU-bound tasks that need to run concurrently.
  - Use `concurrent.futures.ThreadPoolExecutor` if necessary.

- **Task Queues (Future Enhancement)**
  - Consider integrating a task queue like Celery for long-running background
    tasks.

---

## **Project Code Outline**

### **Module Enumeration and Functionality**

1. **`main.py`**
   - Entry point of the application.
   - Initializes the FastAPI app and includes routers.

2. **`api` Package**
   - **`api/__init__.py`**
     - Initializes the API package.
   - **`api/routes.py`**
     - Defines API endpoints and includes routers.
   - **`api/dependencies.py`**
     - Contains dependency injection for requests (e.g., database sessions,
       authentication).

3. **`services` Package**
   - **`services/__init__.py`**
     - Initializes the services package.
   - **`services/business_logic.py`**
     - Implements app-specific business logic functions.
   - **`services/auth.py`**
     - Manages authentication and session logic.

4. **`core` Package**
   - **`core/__init__.py`**
     - Initializes the core package.
   - **`core/agents.py`**
     - Defines agents using LangChain.
   - **`core/chains.py`**
     - Defines chains for sequences of operations.
   - **`core/tools.py`**
     - Implements tools that agents and chains can use.

5. **`models` Package**
   - **`models/__init__.py`**
     - Initializes the models package.
   - **`models/user.py`**
     - Defines the User model.
   - **`models/session.py`**
     - Defines session or state models.
   - **`models/schemas.py`**
     - Defines Pydantic schemas for request and response validation.

6. **`database` Package**
   - **`database/__init__.py`**
     - Initializes the database package.
   - **`database/connection.py`**
     - Manages database connections.
   - **`database/crud.py`**
     - Implements CRUD operations using the repository pattern.

7. **`config.py`**
   - Contains configuration settings and environment variable management.

8. **`utils` Package**
   - **`utils/__init__.py`**
     - Initializes the utils package.
   - **`utils/logger.py`**
     - Sets up application logging.
   - **`utils/exceptions.py`**
     - Defines custom exceptions and error handlers.

---

## **Module Design Details and Boilerplate Implementations**

### **1. `main.py` (Entry Point)**

**Responsibilities:**

- Initialize the FastAPI app.
- Include routers from the API package.
- Set up middleware (e.g., CORS, authentication, sessions).

### **2. `api` Package**

**Responsibilities:**

- Define API endpoints.
- Handle request and response schemas.
- Manage dependencies (e.g., authentication).

### **3. `services` Package**

**Responsibilities:**

- Implement business logic.
- Coordinate between API, core, and data access layers.
- Handle non-LLM processing.

### **4. `core` Package**

**Responsibilities:**

- Integrate LangChain components (agents, chains, tools).
- Define reusable and app-specific agents, chains, and tools.

#### **4.1 `agents` Module**

#### **4.2 `chains` Module**

#### **4.3 `tools` Module**

### **5. `models` Package**

**Responsibilities:**

- Define database models.
- Create Pydantic schemas for request and response validation.

### **6. `database` Package**

**Responsibilities:**

- Manage database connections and sessions.
- Provide CRUD operations via the repository pattern.

### **7. `config.py` (Configuration)**

**Responsibilities:**

- Manage application settings and environment variables.

### **8. `utils` Package**

**Responsibilities:**

- Provide utility functions such as logging and custom exceptions.

---

**Note to Developers:**

- **Customization**: App-specific logic should be implemented in the `services`
  and `core` modules.
- **Extensibility**: Reusable agents, chains, and tools can be extended or
  composed to meet new requirements.
- **Testing**: Ensure that each module, especially asynchronous functions, is
  thoroughly tested.
- **Documentation**: Maintain code documentation for clarity and ease of
  maintenance.
- **Security**: Implement proper error handling and input validation to
  safeguard against security vulnerabilities.

---

## **Appendix**

### **A. Background on CORS Middleware, Sessions, and Authentication**

#### **Cross-Origin Resource Sharing (CORS) Middleware**

##### **What is CORS?**

CORS is a mechanism that allows a web application running on one domain to
request resources from another domain. Browsers implement CORS policies to
protect users from malicious websites attempting to access data from other
origins without permission.

##### **Why is CORS Important?**

When developing a frontend and backend that run on different domains or ports
(e.g., `localhost:3000` for React and `localhost:8000` for FastAPI), browsers
will block cross-origin requests unless the server explicitly allows them.

##### **Support by FastAPI**

FastAPI provides a `CORSMiddleware` that can be added to the application to
specify which origins are allowed to make requests.

##### **Implementation Example:**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Sessions and Authentication**

##### **Authentication Methods**

- **Token-Based Authentication**: Uses tokens (e.g., JWT) to authenticate users.
  Tokens are sent with each request, typically in the `Authorization` header.
- **Session-Based Authentication**: Maintains a session on the server side,
  often using cookies to store session IDs.

##### **Why Authentication Matters**

Authentication ensures that only authorized users can access certain endpoints
or perform specific actions. It is crucial for protecting user data and
application integrity.

##### **How FastAPI Helps**

FastAPI offers integrations with authentication schemes, including OAuth2 and
JWT. It provides utilities like `OAuth2PasswordBearer` to handle token-based
authentication.

**Implementation Example:**

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token and retrieve user
    user = await get_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user
```

#### **Sessions Management**

While FastAPI does not provide built-in session management like some frameworks
(e.g., Django), sessions can be managed using third-party libraries or custom
implementations.

**Possible Approaches:**

- **Custom Session Middleware**: Implement middleware to handle session creation
  and management.
- **Use JWTs**: Stateless authentication using JWT tokens can serve as an
  alternative to sessions.
- **Third-Party Libraries**: Use libraries like `fastapi-login` or
  `fastapi-users` for session management.

**Example with JWT:**

- Users authenticate by providing credentials to a `/token` endpoint.
- Upon successful authentication, the server issues a JWT.
- The client includes the JWT in the `Authorization` header for subsequent
  requests.
- The server validates the JWT on each request to authenticate the user.
