# WorkoutFlow API 

WorkoutFlow API is a FastAPI-based application providing user management functionalities via AWS Cognito, with a PostgreSQL database backend, and endpoints for authentication, profiles, workouts, exercises, and users.
## Table of Contents

- Installation
- Configuration
- Usage
- API Endpoints

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/gagatek1/WorkoutFlow-API.git
    cd WorkoutFlow-API
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory and add the following environment variables:

    ```env
    DATABASE_URL=postgresql://workoutflow:workoutflow@127.0.0.1:5432/workoutflow_db
    REGION_NAME=your_aws_region
    AWS_COGNITO_APP_CLIENT_ID=your_cognito_app_client_id
    AWS_COGNITO_APP_CLIENT_SECRET=your_cognito_app_client_secret
    AWS_COGNITO_USER_POOL_ID=your_cognito_user_pool_id
    ```

2. Ensure that your AWS credentials and region are correctly set up.

## Usage

1. Run the application:

    ```sh
    docker compose up
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication

- **POST /auth/signup**: Sign up a new user.
- **POST /auth/verify**: Verify a user's account.
- **POST /auth/signin**: Sign in a user.
- **POST /auth/token**: Generate a new token.
- **POST /auth/change**: Change a user's password.
- **POST /auth/forgot**: Initiate forgot password process.
- **POST /auth/confirm**: Confirm forgot password.
- **POST /auth/logout**: Log out a user.

### Profiles

- **PUT /profiles/update/{profile_id}**: Update a profile.
- **GET /profiles/{profiles_id}**: Get a specific profile.

### Workouts

- **POST /workouts/create**: Create a new workout.
- **GET /workouts/**: Get all workouts.
- **GET /workouts/{workout_id}**: Get a specific workout.
- **PUT /workouts/update/{workout_id}**: Update a workout.
- **DELETE /workouts/delete/{workout_id}**: Delete a workout.

### Exercises

- **POST /exercises/create**: Create a new exercise.
- **GET /exercises/**: Get all exercises.
- **GET /exercises/{exercises_id}**: Get a specific exercise.
- **PUT /exercises/update/{exercises_id}**: Update a exercise.
- **DELETE /exercises/delete/{exercises_id}**: Delete a exercise.


### Users

- **POST /users/email**: Update a user's email.