import requests
from bs4 import BeautifulSoup



def get_soup(group):
    page = requests.get('http://services.hneu.edu.ua:8081/schedule/schedule?group={}'.format(group))
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def get_data_day(soup, day):
    rows = soup.find('tr')
    # days = rows.find_all('th')
    pair1 = rows.next_sibling
    pair2 = pair1.next_sibling
    pair3 = pair2.next_sibling
    pair4 = pair3.next_sibling
    pair5 = pair4.next_sibling
    pair6 = pair5.next_sibling

    pair1 = pair1.find_all('td',{'id': 'cell'})
    pair2 = pair2.find_all('td',{'id': 'cell'})
    pair3 = pair3.find_all('td',{'id': 'cell'})
    pair4 = pair4.find_all('td',{'id': 'cell'})
    pair5 = pair5.find_all('td',{'id': 'cell'})
    pair6 = pair6.find_all('td',{'id': 'cell'})

    list_pair = [pair1, pair2, pair3, pair4, pair5, pair6]
    # for item in list_pair:
    # 	print(item[3])
    # 	print('--------------------------------------')
    if day == 'mo':
        return scraping_day(list_pair, 0)
    elif day == 'tu':
        return scraping_day(list_pair, 1)
    elif day == 'we':
        return scraping_day(list_pair, 2)
    elif day == 'th':
        return scraping_day(list_pair, 3)
    elif day == 'fr':
        return scraping_day(list_pair, 4)





def scraping_day(list_pair, number_of_day):
    pa = 1
    day_dict = {}
    for par in list_pair:
        if not par[number_of_day].find('div', {'id':'empty'}):
            subject = par[number_of_day].find('td', {'id': 'subject'}).text
            lessonType = par[number_of_day].find('td', {'id': 'lessonType'}).text
            room = par[number_of_day].find('td', {'id': 'room'}).text
            teacher = par[number_of_day].find('td', {'id': 'teacher'}).find('a').attrs['title']
            data = {
            "subject":subject,
            "lessonType":lessonType,
            "room":room,
            "teacher":teacher,
            }
            day_dict[str(pa)] = data
            pa += 1
        else:
            day_dict[str(pa)] = "нет пары"
            pa += 1

    return day_dict




def get_schedule(group, day_of_week):
    soup = get_soup(group)
    day_schedule = get_data_day(soup, day_of_week)
    return day_schedule