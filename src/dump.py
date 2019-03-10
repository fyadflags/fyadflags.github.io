#!/usr/bin/env python3

import os, sys, json, requests, time

this_session = 0
new_this_session = 0

db = {}
if os.path.exists('dump.json'):
    with open('dump.json', 'r') as f:
        try:
            db = json.load(f)
        except Exception as e:
            print(e)

db['flags'] = db.get('flags', {})
db['uniques'] = db.get('uniques', 0)
db['count'] = db.get('count', 0)

try:
    while True:
        result = requests.get('https://forums.somethingawful.com/flag.php?forumid=26').json()
        path = result['path']

        db['count'] += 1
        this_session += 1
        if path not in db['flags']:
            db['flags'][path] = {
                'count': 1, **result
            }
            db['uniques'] += 1
            new_this_session += 1
        else:
            db['flags'][path]['count'] += 1

        print('\rdownloaded {:10} unique {:10} this session {:10} new this session {:10} ctrl-c when youre done'.format(db['count'], db['uniques'], this_session, new_this_session), end='')
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
except Exception as e:
    print('\nuhh something went wrong {}'.format(e))

print('\ndumping to disk')
with open('dump.json', 'w') as f:
    json.dump(db, f, sort_keys=True, indent=4)
print('dumped')
        
