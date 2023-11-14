# Aventus New Site 

A Data entry platform to capture unstructured data into structured data files. The platform will have complete Job allocation, data entry, monitoring and reporting functionality.

# Project Requirements
```
Python >= 3.10.10
Django >= 4.1.7
```

## Installation

Follow these commands step by step


```python
# clone git repository
git clone https://wbgit.workbank.com/ushas/aventus-backend.git

# move to project root diretory
cd aventus

# create virtual env
python -m venv venv

# activate virtual env
   #linux
     source/bin/activate
   #windows 
     venv/Scripts/activate


# install and upgrade pip
python -m pip install --upgrade pip

# install project requirements
pip install -r requirements.txt



# copy '.env.example' and rename '.env.example' to '.env'
# create postgresql database
# set database credentials in '.env' file

# run local server
python manage.py runserver

