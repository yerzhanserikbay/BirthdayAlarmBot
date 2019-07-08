import pymongo


client = pymongo.MongoClient(['MONGO'])

db = client.data


def upload(json_content):
    db.groups.insert_one(json_content)
    print('uploaded')


def push(json_user):
    db.groups.update_one({'group_id': json_user['group_id']},
                         {'$push': {'users': json_user['users']}, "$currentDate": {"lastModified": True}})
    print('pushed')


def update(json_content):
    db.groups.update_one({"group_id": json_content['group_id'],
                          'users': {'$elemMatch': {'user_id': json_content['users']['user_id']}}
                          },
                         {"$set": {
                             'users.$': json_content['users']
                         }, "$currentDate": {"lastModified": True}})
    print('updated')


def get(group_id):
    return db.groups.find_one({'group_id': group_id})['users']


# groups_base = db.groups.find({})

def check(json_content):
    print('checking')
    group_id = json_content['group_id']
    user_id = json_content['users']['user_id']

    group_exist = db.groups.find_one({'group_id': group_id})
    user_exist = db.groups.find_one({'users.user_id': user_id})

    if group_exist is None:
        upload(json_content)
    elif user_exist is None:
        push(json_content)
    else:
        update(json_content)