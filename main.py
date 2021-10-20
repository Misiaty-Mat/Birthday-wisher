import smtplib
import datetime as dt
from random import randint
import pandas

# Enter e-mail account from wich you wish to send wishes
EMAIL_SENDER = "REPLACE WITH YOUR E-MAIL"
PASSWORD = "REPLACE WITH YOUR PASSWORD FOR E-MAIL ACCOUNT"

someone_birthday_today = False

# Checking todays date
now = dt.datetime.now()
current_month = now.month
current_day = now.day

# CSV export
birthdays_data = pandas.read_csv("birthdays.csv")

# Looping through each person data
for person_index in range(0, len(birthdays_data)):
    person_data = birthdays_data.loc[[person_index]]
    birthday_month = int(person_data.month)
    birthday_day = int(person_data.day)

    # Looking if today is someones birthday
    if birthday_month == current_month and birthday_day == current_day:
        someone_birthday_today = True

        # Getting e-mail and name of the person with special day
        e_mail_recever = person_data.email.values[0]
        person_name = person_data.name.values[0]
        print(f"Today it is {person_name} birthday!")

        # Chosing random letter
        rand_letter = f"letter_templates\letter_{randint(1,3)}.txt"

        # Changing letter to contain a name of celebrant
        with open(rand_letter) as letter:
            letter_content = letter.readlines()
            letter_content[0] = letter_content[0].replace("[NAME]", person_name)
            fixed_letter = ""
            for line in letter_content:
                fixed_letter = fixed_letter + line + "\n"

        # Sending e-mail
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL_SENDER, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_SENDER, to_addrs=e_mail_recever, msg=fixed_letter
            )
            print("Wishes sended")


if someone_birthday_today == False:
    print("Today no one from the file have birthday")
