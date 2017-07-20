# logs_analysis_project
 This is a Udacity Project 3 : Logs Analysis Project !

## This project includes:
- news.py
- output.txt
- README.md

## To Run

### You will need:
- python3/python2
- Vagrant
- VirtualBox

### Setup
1. Install psql using command `sudo apt-get install postgresql postgresql-contrib`
2. Set up the user and database(news) using command `sudo -u news psql user_name`
3. Load the data using command `psql -d news -f newsdata.sql`

Alternatively you can use Vagrant and Virtual Box. 

To execute the program, run `python3 newsdata.py` from the command line.

## Author
**Vasu Sheoran**