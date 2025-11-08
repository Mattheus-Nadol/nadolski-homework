"""
======== lekcja 6 ========
Przerób program na dziennik, tak aby używać funkcji
4. Potypuj chociaż jedną funkcje w dzienniku

"""
import pprint # Celem wyprintowania słownika w bardziej eleganckiej formie

def show_grades_list() -> None:
    """Funkcja wyświetla aktualną bazę ocen wszystkich studentów (dictionary)"""
    pprint.pprint(grades_list_school)

def add_subject() -> None:
    """Funkcja dodaje nowy przedmiot (string - key) z miejscami dla studentów (dictionary) do bazy ocen (dictionary), 
    oraz (opcjonalnie) dodaje wszystkich istniejących studentów (dictionary) do tego przedmiotu"""
    new_subject = input("Podaj przedmiot: ")
    if new_subject in grades_list_school:
        print("Przedmiot już istnieje")
    else:
        grades_list_school[new_subject] = {}
        print(f"√ Dodano przedmiot '{(new_subject)}' oraz wszystkich studentów.")
        for dict_of_students in grades_list_school.values():
            for student in dict_of_students.keys():
                if student in grades_list_school[new_subject]:
                    pass
                else:
                    grades_list_school[new_subject].update({student:[]})       

def add_student() -> None:
    """Funkcja dodaje nowego studenta (string - key) z miejscami na oceny (list - values) do wszystkich przedmiotów (dictionaries)"""
    read_student = input("-->Imie studenta: ")
    for subject, dict_of_students in grades_list_school.items():
        if read_student in dict_of_students:
            print(f"'{read_student} ' już jest zapisany/a na: {subject}")
        else:
            print(f"'{read_student}' został(a) zapisany/a na: {subject}")
            grades_list_school[subject].update({read_student:[]})  

def add_grade() -> None:
    """Funkcja dodaje ocenę (int) do listy ocen (list)"""
    read_subject = input("-->Do jakiego przedmiotu?: ")
    if read_subject in grades_list_school:
        read_student = input("-->Dla jakiego studenta?: ")
        if read_student in grades_list_school[read_subject]:
            new_grade = int(input("-->Podaj ocene: "))
            grades_list_school[read_subject][read_student].append(new_grade)
            print(f"√ Dodano ocenę '{new_grade}' do przedmiotu '{read_subject}' dla studenta '{read_student}'.")
        else:
            print(f"Nie ma studenta: '{read_student}' dla przedmiotu '{read_subject}'")   
    else:
        print("Przedmiot nie istnieje, wroc i dodaj go w opcji '1'.")

def calc_aver_subj_stu() -> None:
    """Funkcja oblicza średnią ocen(float) dla wybranego przedmiotu dla wybranego studenta"""
    read_subject = input("-->Z jakiego przedmiotu?: ")
    if read_subject in grades_list_school:
        read_student = input("-->Dla jakiego studenta?: ")
        if read_student in grades_list_school[read_subject]:
            if len(grades_list_school[read_subject][read_student]) == 0:
                print(f"Brak ocen do wyliczenia średniej dla przedmiotu '{read_subject}'")
            else: 
                avg_subj_stu = sum(grades_list_school[read_subject][read_student]) / len(grades_list_school[read_subject][read_student])
                print(f"Średnia ocen z przedmiotu '{read_subject}' dla '{read_student}' to '{avg_subj_stu:.1f}'")
        else:
            print(f"'{read_student}' nie został(a) zapisany/a na: '{read_subject}'") 
    else:
        print("Przedmiot nie istnieje, wróć i dodaj go w opcji '1'.")    

def calc_aver_stu() -> None:
    """Funkcja oblicza średnią ocen (float) ze wszystkich przedmiotów dla wybranego studenta"""
    list_averages = []
    read_student = input("-->Dla jakiego studenta?: ")
    for subject, dict_of_students in grades_list_school.items():
        for name, grades in dict_of_students.items():
            if read_student in name:
                if len(grades) == 0:
                    print(f"Student {read_student} nie ma ocen w przedmiocie {subject}")
                else:    
                    avg_stu_subj = sum(grades) / len(grades)
                    # print(f"Srednia dla '{name}' z przedmiotu '{subject}' to '{avg_student_partial:.1f}' - obliczanie koncowej...")
                    list_averages.append(avg_stu_subj)
            else:
                pass
    if len(list_averages) == 0:
        print(f"Brak ocen do policzenia średniej dla studenta '{read_student}'")
    else:
        avg_stu = sum(list_averages) / len(list_averages)
        print("*"*15, end=" ")
        print(f"Średnia studenta '{read_student}' ze wszystkich przedmiotów to: '{avg_stu:.1f}'")

def calc_aver_subj() -> None:
    """Funkcja oblicza średnią ocen (float) dla wybranego przedmiotu dla wszystkich studentów"""
    list_averages = []
    read_subject = input("-->Z jakiego przedmiotu?: ")
    if read_subject in grades_list_school:
        for name, grades in grades_list_school[read_subject].items():
            if len(grades) == 0:
                print(f"Student {name} nie ma ocen w przedmiocie {read_subject}")
            else:
                avg_subj_stu = sum(grades) / len(grades)
                list_averages.append(avg_subj_stu)
        if len(list_averages) == 0:
            print(f"Brak ocen z przedmiotu {read_subject}")
        else:
            avg_subj = sum(list_averages) / len(list_averages)
            print("*"*15, end=" ")
            print(f"Średnia z przedmiotu {read_subject} to: {avg_subj:.1f}")              
    else:
        print("Przedmiot nie istnieje, wróć i dodaj go w opcji '1'.") 

def calc_aver() -> None:
    """Funkcja oblicza średnią ocen (float) dla wszystkich przedmiotu dla wszystkich studentów"""
    list_averages = []
    for subject, dict_of_students in grades_list_school.items():
        for name, grades in dict_of_students.items():
            if len(grades) == 0:
                print(f"'{name}' nie ma ocen z przedmiotu '{subject}'")
            else:
                avg_subj_stu = sum(grades) / len(grades)
                list_averages.append(avg_subj_stu)
    if len(list_averages) == 0:
        print("Brak ocen do policzenia średniej ogólnej")
    else:
        avg_total = sum(list_averages) / len(list_averages)
        print("*"*15, end=" ")
        print(f"Średnia ogólna to: {avg_total:.1f}")

def print_options() -> None: 
    """Funkcja wyświetla listę opcji wyboru"""
    print("OPERACJE BAZY STUDENTÓW:") 
    print("1 - dodaj przedmiot")
    print("2 - dodaj ocenę")
    print("3 - policz średnią z jednego przedmiotu dla jednego studenta")
    print("4 - policz średnią z jednego przedmiotu dla wszystkich studentów")
    print("5 - policz średnią ze wszystkich przedmiotów dla jednego studenta")
    print("6 - policz średnią ogólną ze wszystkich przedmiotów dla wszystkich studentów")
    print("7 - dodaj studenta")
    print("OPCJE DODATKOWE:") 
    print("B - Wyświetl aktualną bazę ocen")
    print("H - Wyświetl ponownie listę opcji")
    print("Z - zakończ")

grades_list_school = { # Baza (słownik) z ocenami wszystkich studentów 
    "matematyka": {
        "Ada": [5, 5, 4],
        "Jarek": [4, 4, 6],
        "Monika": [4, 5, 3],
    },
    "polski": {
        "Ada": [4, 3, 6],
        "Jarek": [4, 5, 6],
        "Monika": [4, 5, 6],
    },
    "angielski": {
        "Ada": [4, 5, 6],
        "Jarek": [6, 5, 3],
        "Monika": [4, 4, 6],
    },
    "historia": {
        "Ada": [3, 3, 2, 1],
        "Jarek": [4, 4, 6],
        "Monika": [6, 5, 3],
    },
    "geografia": {
        "Ada": [6, 5, 3],
        "Jarek": [4, 4, 6],
        "Monika": [6, 5, 3],
    },
    "biologia": {
        "Ada": [1, 6, 2],
        "Jarek": [6, 1, 2],
        "Monika": [2, 4, 1],
    },
}


print_options() # Lista opcji wyboru | Poza pętlą, aby nie wyskakiwały za każdym razem
while True:
    user_choice = input("WYBIERZ OPERACJĘ (1-7) lub OPCJĘ: (B)aza, (H)elp, (Z)akończ : ") # Ten komunikat wyskoczy za każdym razem
    if user_choice == "B" or user_choice == "b": # OPCJA B - Wyświetlenie całej bazy ocen...
        show_grades_list()

    elif user_choice == "1": # OPCJA 1 - Dodawanie przedmiotu...
        print("1 - Dodawanie przedmiotu...")
        add_subject()
        
    elif user_choice == "2": # OPCJA 2 - Dodawnie oceny...
        print("2 - Dodawnie oceny...")
        add_grade()

    elif user_choice == "3": # OPCJA 3 - Liczenie średniej z jednego przedmiotu dla jednego studenta...
        print("3 - Liczenie średniej z jednego przedmiotu dla jednego studenta...")
        calc_aver_subj_stu()

    elif user_choice == "4": # OPCJA 4 - Liczenie średniej z jednego przedmiotu dla wszystkich studentów...
        print("4 - Liczenie średniej z jednego przedmiotu dla wszystkich studentów...")
        calc_aver_subj()

    elif user_choice == "5": # OPCJA 5 - Liczenie średniej ze wszystkich przedmiótow dla jednego studenta...
        print("5 - Liczenie średniej ze wszystkich przedmiotów dla jednego studenta...")
        calc_aver_stu()

    elif user_choice == "6": # OPCJA 6 - Liczenie średniej ze wszystkich przedmiotów dla wszystkich studentów...
        print("6 - Liczenie średniej ze wszystkich przedmiotów dla wszystkich studentów...")
        calc_aver()

    elif user_choice == "7": # OPCJA 7 - Dodawanie studenta...
        print("7 - Dodawanie studenta...")
        add_student()

    elif user_choice == "Z" or user_choice == "z": # OPCJA Z - Zakończenie programu...
        print(">>> Dziękujemy za skorzystanie z listy studentów <<<\n>>> KONIEC <<<")
        break
    
    elif user_choice == "H" or user_choice == "h": # OPCJA H - Ponowne wyświetlenie listy opcji
        print_options()

    else:
        print("Błędny wybór, spróbuj ponownie")        
