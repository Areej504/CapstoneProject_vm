@echo off
REM Create a virtual environment if it doesn’t exist
if not exist venv (
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies from requirements.txt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Deactivate the virtual environment
deactivate

echo Dependencies installed successfully.
