# Seven.Travel Test task

## Description
A simple FastAPI application with CRUD endpoints for working with tasks. You can create tasks, get a list of tasks (including those sorted by task status), edit and delete tasks. 

## Demo

To demonstrate the API, the Postman collection has been added to the repository.

---
## Setup and launch
To run the application, you need to download the repository to the machine
(you don't need to download the setup.cfg files and the /tests/ folder).
After that, add the environment variables (you can add them to the file .env)
based on the example from the .env.example file. Finally, to lift the application from the database,
you need to run the ```docker compose up --build``` command.
If the application is deployed on a local machine, the API will be available at http://localhost:8000/.
To deploy the application on a remote server, you need to clone the project and run the same commands.
___

## Endpoints

- **GET /tasks/** - Get all tasks
- **GET /tasks/?status=<todo, in_progress or done>** - Get all tasks with the status
- **POST /tasks/** - Create a new task
- **GET "/tasks/{task_id}/"** - Get the task by id
- **PUT "/tasks/{task_id}/"** - Update the task
- **DELETE "/tasks/{task_id}/"** - delete the task

For more detailed documentation, you can use Swagger (http://localhost:8000/docs )
___

## Stack
- FastAPI
- Postgres
- SQLAlchemy
- Docker
- Swagger
- Postman
