@echo off
echo Installing necessary Python packages...
echo.
echo  -------------------------
echo  ^|                       ^|
echo  ^|   Installing...      ^|
echo  ^|                       ^|
echo  -------------------------
echo.
python -m pip install --upgrade pip
pip install PyQt5 requests pyperclip
echo.
echo  -------------------------
echo  ^|                       ^|
echo  ^|   Installation       ^|
echo  ^|   complete!          ^|
echo  ^|                       ^|
echo  -------------------------
echo.
pause
