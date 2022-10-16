# PPII2 «Projet Pluridisciplinaire d'Informatique Intégrative» 2 (2021-2022)

Professor : 
Olivier Festor <<olivier.festor@telecomnancy.eu>>  
Gérald Oster <<gerald.oster@telecomnancy.eu>>

## Context

This is a 4 person project done in the second semester of the first year in Telecom Nancy. 

## WORDLE

**E32 group** :

- **Valentin CHANEL**
- Matéo DEMANGEON
- Nicolas FRACHE
- Victor VOISIN

## Description

First, we created a wordle web application ( like : https://www.nytimes.com/games/wordle/index.html ) with Python / Flask / SQLite / Html / CSS / JavaScript.

Then we wrote and optimize a solver in C, using ![information theory](https://youtu.be/v68zYyaEmEA) and advanced data structure.

[Here is the original subject](./documents/sujet.pdf) ( in French ).

## Part 1 - Web Application

### Initialization :

1. Clone the git repository on yout computer.


2. In the ```./app_wordle/``` folder, create a virual environnement :
   ```python3 -m venv ./venv```.


3. Enter the virtual environnement :
    - Linux / Mac: ```source ./venv/bin/activate```
    - Windows: ```.\venv\Scripts\activate.bat```

4. Install dependancies: ```pip install -r requirements.txt```.


5. Initialiaze the database: ```flask initdb```.


6. To launch the app, you can either use:
    -  ```flask run -p 3000```
    - or  ```python3 app.py```,but with this method you can't choose the port.


7. Finaly to test it, use the url: http://localhost:3000/.

#### To use the automated test:

- Use the ```pytest``` command.

## Part 2 - C Solver

### Prerequisite :

- Clang compiler : ````sudo apt install clang````
- SQLite 3 library for C : ````sudo apt-get install libsqlite3-dev````

### Compilation and execution

- In the solveur folder, use : ````make solver```` and ````make test````.
- To execute the automated test, go in the "/bin" folder and type : ````./solver```` or ````./test````

### Choose a Word :

- Our dictionnary is from the Lexique3 database and is very complete, every french word is guessable.

## Conventions on commit commentary :

In order to clarify commit goal, we used a modified version of ![this](https://github.com/ahmadawais/Emoji-Log/) convention.

*The use of emoticon increase visibilty.*

1. `✨ NEW: MESSAGE`
   > New functionality.

2. `🔨 IMPROVE: MESSAGE`
   > Improvement or refactoring of existing code.

3. `🪲 FIX: MESSAGE`
   > Bug fixing.

4. `💡 DOC: MESSAGE`
   > Documentation.

5. `🤖 TEST:MESSAGE`
   > Everything linked to testing.

6. `🐎 PERF: MESSAGE`
   > Performance measurement.

7. `📚 GDP: MESSAGE`
   > Project management file.

8. `🔀 MERGE: MESSAGE`
   > Branch merging

9. `🔧 CONF: MESSAGE`
   > Config file

10. `🚧 WIP: MESSAGE`
    > **Work in progress**

11. `💄 COS: MESSAGE`
    > Cosmetic change

12. `📌 RELEASE: MESSAGE`
    > Working prototype

## Credit

The ReadMe was updated by Nicolas Frache and then translated and modified by Valentin CHANEL.
