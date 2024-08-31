FROM python:3.11

# Setează variabila de mediu pentru a preveni interacțiunea cu prompturile în timpul instalării
ENV PYTHONUNBUFFERED 1

# Creează un director de lucru pentru aplicație
WORKDIR /app

# Copiază fișierele requirements.txt în directorul de lucru
COPY requirements.txt /


# Copiază toate fișierele aplicației în directorul de lucru
COPY . /app/

# Expune portul pe care serverul Django va rula
EXPOSE 8000

# Comanda de rulare a serverului Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
