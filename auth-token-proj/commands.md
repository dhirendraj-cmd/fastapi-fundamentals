pip install "fastapi[standard]"
pip install sqlmodel
pip install python-jose[cryptography]
pip install passlib[bcrypt]
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
