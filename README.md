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
    -H 'Authorization: Bearer <bearer_token>'
    ```

3. Documented & tested with swagger:
    * Localhost run:
    ```sh
    http://127.0.0.1:8000/docs
    ```
    <img width="701" alt="image" src="https://github.com/binhlam/todo/assets/19790314/b9eeb48e-bda7-44f8-b800-d6aa3abf5d53">

    <img width="1346" alt="image" src="https://github.com/binhlam/todo/assets/19790314/5c2e78d9-f698-4807-a71d-c072636f3d2a">
