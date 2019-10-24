import requests
import json
import datetime
from collections import Counter

#for detailed info cheсk file instruction.txt

#write your page addres(id) in vk
MY_ID=''
#write your secret token
ACCESS_TOKEN = ''
VERSION = '5.102'
NOW=datetime.datetime.now()
#simple method for getting add info
URL_USERS_GET = 'https://api.vk.com/method/users.get'
URL_FRIENDS_GET = 'https://api.vk.com/method/friends.get'

BASE_LOAD={'v':VERSION,'access_token':ACCESS_TOKEN}

#in this func i get user(your id...) and return all dbate friends
def get_all_friends(my_id):
    #make request for getting info about friends
    r1 = requests.get(URL_FRIENDS_GET,
    params={**{'user_ids':my_id},**BASE_LOAD})

    #thanks json get total count and id friends
    friends_id=r1.json()['response']['items']
    friends_count=r1.json()['response']['count']

    friends_bdate=[]
    for i in range (friends_count):
        #add param fields(that be get bdate )
        r1=requests.get(URL_USERS_GET,
            params={**{'user_ids':friends_id[i],'fields':'bdate'},**BASE_LOAD})
        try:
            #add only bdate in list
            friends_bdate.append(r2.json()['response'][0]['bdate'])
        except:
            #if user hid info about bdate,than i just skipping him
            pass
    return friends_bdate

#in this func i get all bdate friends from user(your id...)
#and return ordered dict with age and number of friends with this age
def get_difference_beetwen_bdate(bdate):
    #list for save differance
    count_repetition=[]

    for i,item in enumerate(bdate):
        #creat list where split is .(becouse i should separate bdate for next opperathion)
        item=item.split('.')
        #transform in int format
        bdate[i]=[eval(x) for x in item]
        try:
            count_repetition.append(NOW.year-bdate[i][2])
            if NOW.month-bdate[i][1]>0 or NOW.month==bdate[i][1] and NOW.day>bdate[i][0]:
                pass
            else:
                count_repetition[i]-=1
        except:
            #if user hid info about bdate
            count_repetition.append('Incomplete format')

    return Counter(count_repetition)

if __name__ == '__main__':
    all_date=get_all_friends(MY_ID)
    dict_with_means=get_difference_beetwen_bdate(all_date)
    dict_with_means.pop('Incomplete format')
    print('Age','\t','Number of people with this age:')
    for i in (dict_with_means.keys()):
        print(i,'\t\t',dict_with_means[i])
