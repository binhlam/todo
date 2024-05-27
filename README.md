## Developing a server side CRUD application including JWT authorization with FastAPI
### Created date: 2024-05-20
### Author: *Binh Lam*

# Environment Setup
1. Run the server-side with Virtualenv:
    * Activate Virtualenv
    ```sh
    cd ~/<your-path>/todo
    python3 -m venv todo_env
    source todo_env/bin/activate
    pip install -r requirements.txt
    ```
    * Api Run:
    ```sh
    cd ~/<your-path>/virtualenvs/todo_env/bin
    uvicorn app.main:app --reload
    ```

2. Sample curl:
    ```sh
    curl -X 'GET' \
    'http://127.0.0.1:8000/v1/users/1' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjAxIiwiaWQiOjEsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcxNjc5NjY4N30.XOBNXM6wtv87khJwGynOnZWD9ztrDoo_fxDGB23LWJ4'
    ```

3. Documented & tested with swagger:
    * Api Run:
    ```sh
    http://127.0.0.1:8000/docs
    ```
