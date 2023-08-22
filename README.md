**Challenge Prompt**

Your goal is to build a simple blogging app. It should allow the user to create new blog posts, edit existing posts,
and view all existing posts. Let’s assume this user is a minimalist; plaintext posts are all that they care about. Let’s also assume this user is
very private and intends to only host this on their local machine for themselves; no need for authentication.
Your teammate has already built most of the UI and is now handing it off to you to integrate with the backend you’re
building. Ideally, your backend should be built using FastAPI and SQLite, however any framework built in Python or PHP is
acceptable.

-----------------------------------------------

**Set up**

Make sure you have fastapi and uvicorn installed

Here are the commands to install if you are missing any

`pip install fastapi`

`pip install uvicorn`

**Testing**

To run the tests you can use pytest, or whatever debugger you normally use

If you need to install pytest the command is

`pip install -U pytest`

To run the tests in the command line just run command `pytest` to run all tests

*The unit tests have to be run all together in one session because currently the tests depend on the results of earlier tests (virtual database records). The tests will fail if run individually. This is not ideal but it works for now


**Running the Server**

To run the app in the cmdline run 

`uvicorn api_app.main:app --reload`

This should run the server on  http://127.0.0.1:8000 
