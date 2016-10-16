import datetime
import csv

# Set global variables
datetime_date = ""
subject = ""
chapters = ""
subjecttype = ""

#Pharm specific
pharmpages = ""
num_drugs = ""

#Path specific
patopages = ""

#.csv writer variables
file_name = "tasks.csv"
output_file = ""
output_writer = ""



def init():
    command = input("Add or clear? [a/C] ")
    global output_file
    global output_writer
    if command == "a":
        print("Adding to planning")
        output_file = open(file_name, mode='a')
        output_writer = csv.writer(output_file)
        change_date()
    elif command == "C":
        output_file = open(file_name, mode='w') #First clear it
        output_file = open(file_name, mode='a') #Then append from now on
        output_writer = csv.writer(output_file)
        output_writer.writerow(['TYPE', 'CONTENT', 'PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG'])
        msg = "Clearing {}".format(file_name)
        print(msg)
        change_date()
    else:
        msg = "I do not understand '{}'".format(command)
        print(msg)
        init()


def change_date():
    command = input("Date? ")
    global datetime_date
    datetime_date = datetime.datetime.strptime(command, "%d/%m")
    change_subject()


def change_subject():
    command = input("Subject? (eg. cardiovascular) ")
    global subject
    subject = command
    change_chapter()


def change_chapter():
    command = input("Chapter(s)? ")
    global chapters
    chapters = command
    choose_type()


def choose_type():
    command = input("Type? [ff, fh, pf, ph] ")
    global subjecttype
    subjecttype = command
    if command == "ff":
        ff()
    elif command == "fh":
        fh()
    elif command == "pf":
        pf()
    elif command == "ph":
        ph()
    else:
        msg = "I do not understand '{}'".format(command)
        print(msg)
        choose_type()

def ff():
    command = input("How many pages in chapter? ")
    clear_unique()
    global pharmpages
    pharmpages = int(command)

    command2 = input("How many new drugs? ")
    global num_drugs
    num_drugs = int(command2)
    write_to_csv()


def fh():
    clear_unique()
    write_to_csv()


def pf():
    clear_unique()
    command = input("How many pages in chapters? ")
    global patopages
    patopages = int(command)
    write_to_csv()


def ph():
    clear_unique()
    write_to_csv()

#The task_write function
def task_writer(description, priority, day_delta, duration, time_quotient):
    duration_formatted = str(duration * time_quotient) #Multiply duration by quotient to compensate

    task_date = datetime_date + datetime.timedelta(days=day_delta) #Calculate time for task
    formatted_date = datetime.datetime.strftime(task_date, "%d/%m") #Format date back to DK/todoist friendly
    task_description = description + " " + subject + " @fokus" + " (Cp. " + chapters + ") " + duration_formatted #Frankenstein the task_description

    output_writer.writerow(['task', task_description, priority, 1, '', '', formatted_date, 'dk']) #Write the row

def write_to_csv():
    # Write date, subject, chapters, pages to .csv
    msg = "Writing to .csv"
    print(msg)
    if subjecttype == "ff":
        #Planlægge at se SketchyPharm videoer 3 dage før forelæsninger.
        task_writer("Læse farmakapitler", "1", -3, pharmpages, 4)

        #Planlægge at gennemgå http://farma.morsby.dk og lave flashcards 3 dage før forelæsning
        task_writer("(Husk Sketchy/egne memory-hooks & brug farma.morsby.dk) Lav og repetér first-pass flashcards med navne til", "2", -3, num_drugs, 4)

        #Lave second-pass flashcards dagen efter forelæsningen
        task_writer("Lav og repetér second-pass farmaflashcards til", "2", 1, 15, 1)

        done()
    elif subjecttype == "fh":
        #Planlægge at laver opgaver dagen før holdtimen
        task_writer("Lave opgaver til farmaholdtimen i", "3", -1, 30, 1)

        #Planlægge at lave second-pass flashcards dagen efter holdtimen
        task_writer("Lave flashcards fra farmaholdtimen i", "3", 1, 10, 1)

        done()
    elif subjecttype == "pf":
        #Planlægge at se SketchyPharm videoer 3 dage før forelæsninger.
        task_writer("Læse pato-kapitel om", "1", -3, patopages, 3)

        #Planlægge at gennemgå http://farma.morsby.dk og lave flashcards 3 dage før forelæsning
        task_writer("Lave first-pass flashcards til pato-kapitel om", "2", -3, patopages, 1.5)

        #Lave second-pass flashcards dagen efter forelæsningen
        task_writer("Lav og repetér second-pass patoflashcards til", "2", 1, 20, 1)
        done()

    elif subjecttype == "ph":
        #Planlægge at laver opgaver dagen før patoholdtimen
        task_writer("Lave opgaver til patoholdtimen i", "3", -1, 40, 1)

        #Planlægge at lave second-pass flashcards dagen efter holdtimen
        task_writer("Lave flashcards fra patoholdtimen i", "2", 1, 10, 1)
        done()


def done():
    change_date()


def clear_unique():
    global pharmpages
    global patopages
    global num_drugs
    pharmpages = ""
    patopages = ""
    num_drugs = ""

init()
