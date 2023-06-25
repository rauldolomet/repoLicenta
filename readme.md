# THREAT DETECTIVE Web API

Acesta este un ghid pentru instalarea și rularea THREAT DETECTIVE Web API prin clonarea repo-ului și instalarea dependențelor necesare.

## Instalare și configurare

1. Clonează Repo-ul

   ```
   git clone https://github.com/rauldolomet/repoLicenta.git
   ```

2. Instalează Dependințele

   Navighează în directorul proiectului și instalează dependențele necesare prin următoarea comandă:

   ```
   pip install -r requirements.txt
   ```

   Aceasta va instala bibliotecile necesare specificate în fișierul `requirements.txt`.

3. Rulează Web API-ul

   Odată ce dependențele sunt instalate, rulează următoarea comandă în directorul proiectului pentru a porni THREAT DETECTIVE Web API:

   ```
   flask run --host=0.0.0.0 --debug
   ```

   Serverul va începe să ruleze local, iar tu vei putea accesa endpoint-urile API-ului.
   Alege şi urmareşte oricare din cele doua variante de adrese date in terminal.

## Utilizare

THREAT DETECTIVE Web API te va obliga sa te autentifici înainte de toate. Foloseste aceste credentiale:
username: raul
parola: Raul1611@

După autentificare te invit să alegi Create users sau Scan users. Dacă alegi Create users, introdu datele si urmareste erorile de validare, dacă apar.
Dacă alegi Scan users, foloseşte, ca exemplu, CNP-ul :
SSN: 5001116350065

Incearca şi functionalitatea de alertare, daca eşti curios.


## Concluzie

THREAT DETECTIVE Web API este acum instalat și rulează. Urmează instrucțiunile de instalare menționate mai sus și utilizează exemplele furnizate pentru a interacționa cu API-ul. Serverul va rula local și îl poți accesa prin cereri HTTP.
