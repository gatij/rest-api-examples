# REST-API-Examples

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.0-brightgreen.svg)](https://djangoproject.com)
[![ChartJs Version](https://img.shields.io/badge/chartjs-2.4.0-orange.svg)](https://www.chartjs.org/)

An example project with three small apps explaining the concepts of public REST APIs . 

![RESTful APIs Example Screenshot](https://drive.google.com/file/d/1JK7Q6xFK0wINiKOzlMyDi3LhkxfJ9ZqR/view?usp=sharing)

This project is deployed at [rest-api-examples.herokuapp.com](https://rest-api-examples.herokuapp.com/).

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/gatij/rest-api-examples.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```


Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.


