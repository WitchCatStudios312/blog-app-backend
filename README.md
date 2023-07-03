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

*The unit tests all have to be run one after the other because currently the tests depend on the results of earlier tests (database records)


**Running the Server**

To run the app in the cmdline run 

`uvicorn api_app.main:app --reload`

This should run the server on  http://127.0.0.1:8000 

**Running the Client**

In the command line run

`npm start`
