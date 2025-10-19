@echo off
echo Installing required libraries from requirements.txt...
venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo Starting the Hilbert Curve Mapping Comparator...
cmd /c venv\Scripts\python.exe HilbertCompare.py
