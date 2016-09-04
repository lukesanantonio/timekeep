import argparse
import sqlite3
import sys
import datetime
import humanize

cmd = argparse.ArgumentParser(description="Manage time")
cmd.add_argument('activity', help='Activity to begin')

# TODO:
# - Add script to end an activity.
# - Use another table to keep track of all possible activities. Maybe instead of
# using a string use a foreign key into a table of possible activities.
# - Support activity parenting. For example I should be able to log my
# programming on a specific project, but maintain the fact that I am nonetheless
# programming. At some later point I can go back and see how much time I've
# spent programming and how much of that was spent on particular projects. Maybe
# a kind of "inheritance" isn't a good solution. Maybe each thing can have tags
# and the tags would be the more general thing. Like I would have an activity
# for each project and a tag for Programming.

if __name__ == '__main__':
    args = cmd.parse_args()

    conn = sqlite3.connect('activities.sqlite3')

    # Make sure we have a table
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS activities '
                '(activity text, start_time int, end_time int)')
    conn.commit()

    # Is that activity already open?
    cur.execute('SELECT activity,start_time FROM activities WHERE '
                'activity == ? AND end_time IS NULL', (args.activity,))
    open_activities = cur.fetchall()
    if len(open_activities) == 1:
        # Activity already open!
        activity = open_activities[0]

        name = activity[0]
        readable_time = humanize.naturaltime(
            datetime.datetime.fromtimestamp(activity[1])
        )

        print('You are already doing {} (started {})'
              .format(name, readable_time))
        sys.exit(0)
    elif len(open_activities) > 1:
        print('Something is very wrong; There are {} running activities called'
              ' {}!'.format(len(open_activities), args.activity))

    # Start the activity
    # TODO: Make sure activity is safe, reasonable, etc.
    cur.execute('INSERT INTO activities VALUES (?, strftime("%s", "now"),'
                'null)', (args.activity,))
    conn.commit()

    print('Started {}', args.activity)
