To make a virtual environment:
py -3 -m venv venv

To activate the venv:
.\Scripts\activate

to create requirements file: 
pip freeze > requirements.txt

to reload fastapi after each updation

uvicorn app.main:app --reload

