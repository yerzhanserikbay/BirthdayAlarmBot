import os
import base_manager as bm
import xlsxwriter
from datetime import datetime

cwd = os.getcwd()


def insert_element(data):
    inserted_data = data

    user_id = str(inserted_data[4])

    group_id = str(inserted_data[5])

    # prepare added data

    json_content = {
        "group_id": group_id,
        "users":
            {
                "user_id": user_id,
                "first_name": str(inserted_data[0]),
                "last_name": str(inserted_data[1]),
                "username": str(inserted_data[2]),
                "birthday": str(inserted_data[3])
            }
    }

    bm.check(json_content)


def get_elements(sended_id):
    users = bm.get(sended_id)
    message = ''
    count = 1

    for user in users:
        message += f'-{str(count)}-' + '\n' + 'First Name' + user['first_name']
        message += '\n' + 'Last Name' + user['last_name']
        message += '\n' + 'Username' + user['username']
        message += '\n' + 'Birthday' + user['birthday'] + '\n\n'
        count += 1
    return message


def get_file(sended_id):
    users = bm.get(sended_id)

    users_tuple = ()

    for user in users:
        u = [user['first_name'], user['last_name'], user['username'], user['birthday']]
        users_tuple += u,

    workbook = xlsxwriter.Workbook('Birthdays.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': 1})

    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    worksheet.set_column(0, 0, 5)
    worksheet.set_column(1, 4, 15)

    worksheet.write('A1', 'Count', bold)
    worksheet.write('B1', 'First Name', bold)
    worksheet.write('C1', 'Last Name', bold)
    worksheet.write('D1', 'Username', bold)
    worksheet.write('E1', 'Birthday', bold)

    row = 1
    col = 0
    count = 1

    for fn, ln, un, bd in users_tuple:
        date = datetime.strptime(bd, "%Y-%m-%d")

        worksheet.write(row, col, count)
        worksheet.write(row, col + 1, fn)
        worksheet.write(row, col + 2, ln)
        worksheet.write(row, col + 3, un)
        worksheet.write_datetime(row, col + 4, date, date_format)

        count += 1
        row += 1

    workbook.close()

    cwd = os.getcwd()

    doc = open('{}/Birthdays.xlsx'.format(cwd), 'rb')

    return doc

