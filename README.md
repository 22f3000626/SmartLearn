# EduPath

# PostgreSQL Integration

## Requirements
- PostgreSQL server running locally or remotely
- Update `requirements.txt` and install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Database Configuration
- By default, the app connects to:
  `postgresql://postgres:password@localhost:5432/smartlearn`
- You can override this by setting the `DATABASE_URL` environment variable:
  ```bash
  export DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
  ```
- Create the database manually if it does not exist:
  ```sql
  CREATE DATABASE smartlearn;
  ```

## Initializing Tables
- Tables are created automatically on app startup.

## Example User Model
- A sample `User` model is included for demonstration.