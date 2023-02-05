import datetime
import requests
from sqlitebdmanagement import connectdb
from multiprocessing import Process


class Importdata:
    def __init__(self):
        self.url_groups = "http://80.76.178.21:8053/api/raspGrouplist?year=2022-2023"
        self.url_raspis = "http://80.76.178.21:8053/api/Rasp?idgroup="
        self.group = []
        self.rasp = []

    def add_groups(self):
        response = requests.get(self.url_groups).json()
        k = 0
        for i in response['data']:
            k = k + 1
            group = {"name": i['name'], "group_id": i['id'], "kurs": i['kurs'], "facul": i['facul'], "id": k}
            self.group.append(group)

    def add_all_raspis(self):
        k = 0
        for group in self.group:

            response = requests.get(f"{self.url_raspis}{group['group_id']}").json()
            for i in response['data']['rasp']:
                k = k + 1
                rasp = {'start_time': i['начало'],
                        'start_date': i['датаНачала'],
                        'stop_time': i['конец'],
                        'number_date': i['деньНедели'],
                        'day_week': i['день_недели'],
                        'discipline': i['дисциплина'],
                        'prepod': i['преподаватель'],
                        'audit': i['аудитория'],
                        'group_id': i['кодГруппы'],
                        'updateDay': response['data']['info']['dateUploadingRasp'],
                        'id': k}
                self.rasp.append(rasp)
        print(len(self.rasp))
        print(self.rasp)


    @connectdb
    def groupexecute(self, cursor):
        for i in self.group:
            params = i['name'], i['kurs'], i['facul'], i['group_id']
            cursor.execute("""
                                INSERT INTO Groups(name, 'kurs', 'facul', group_id) 
                                VALUES (?,?,?,?)
                            """, params)

    @connectdb
    def groupupdate(self, cursor):
        for i in self.group:
            cursor.execute("""SELECT kurs FROM Groups WHERE id = ? """, (i['id'],))
            if len(cursor.fetchall()) > 0:
                cursor.execute("""UPDATE Groups SET name = ?, kurs = ?, facul = ?, group_id = ? 
                                  WHERE id = ?""",
                               (i['name'], i['kurs'], i['facul'], i['group_id'], i['id']))
                # print("обновляю шруппу ")
            else:
                cursor.execute("""INSERT INTO Groups(name, 'kurs', 'facul', group_id) 
                                  VALUES (?,?,?,?)
                                  ON CONFLICT DO NOTHING""",
                               (i['name'], i['kurs'], i['facul'], i['group_id']))
                # print("записываю гуруппу")

    @connectdb
    def insertrasp(self, cursor):
        cursor.execute("""DELETE FROM Raspis""")
        for i in self.rasp:
            cursor.execute("""INSERT INTO Raspis(id, start_time, start_date, stop_time, number_date,
                                                                    day_week, discipline, prepod, audit, group_id,
                                                                    update_day)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (i['id'], i['start_time'], i['start_date'], i['stop_time'], i['number_date'], i['day_week'],
                            i['discipline'], i['prepod'], i['audit'], i['group_id'], i['updateDay']))



def updatedb():
    try:
        i = Importdata()
        i.add_groups()
        i.groupupdate()
        i.add_all_raspis()
        i.insertrasp()
        print('РАСПИСАНИЕ ОБНОВЛЕНО')

    except Exception as e:
        print(e)


def startupdate():
    t1 = Process(target=updatedb, args=())
    t1.start()


# def start():
#     timestart = datetime.datetime.now()
#     i = Importdata()
#     i.add_groups()
#     i.groupupdate()
#     i.add_all_raspis()
#     # i.insertrasp()
#     i.raspupdate()
#     stop = datetime.datetime.now()
#     print(stop - timestart)
#
#
# def restart():
#     con = False
#     while con is False:
#         try:
#             start()
#             con = True
#         except Exception as exc:
#             print(exc)
#             con = False

#
# start()
