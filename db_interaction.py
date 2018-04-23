import sqlite3


def db_insert_task(text):
    '''
    :param text: text that we want to insert as task in the db
    This method insert a task in the database
    '''

    # prepare the query text
    sql = """INSERT INTO task(todo) VALUES (?)"""

    #connect to the db
    conn = sqlite3.connect("task_list.db")
    cursor = conn.cursor()
    result = -1
    try:
        #execute the query passing the needed parameters
        cursor.execute(sql, (text, ) )
        #commit all pending queries
        conn.commit()
        result = 1
    except Exception as e:
        print(str(e))
        # if something goes wrong: rollback
        conn.rollback()

    #close the connection
    conn.close()

    return result


def get_sorted_tasks_list():
    '''
    :param tasks_list: list of existing tasks
    Get existing tasks from the database
    '''

    tasks_list = []
    sql = "SELECT todo FROM task order by todo ASC" #here we order data using "order by"
    conn = sqlite3.connect("task_list.db")

    # to remove u from sqlite3 cursor.fetchall() results
    conn.text_factory = sqlite3.OptimizedUnicode


    cursor = conn.cursor()
    cursor.execute(sql)

    results = cursor.fetchall()

    # print results

    for task in results:
        tasks_list.append(task[0]) #each "task" is a tuple, so we have to take the first element of it

    conn.close()

    return tasks_list


def db_contains(task):
    '''
    :param task: the task we want to check
    This method returns true if a given task is in the db, false otherwise
    '''

    # prepare the query text
    sql = "select todo from task where todo = ?"

    # connect to the db
    conn = sqlite3.connect("task_list.db")
    cursor = conn.cursor()
    cursor.execute(sql, (task,))

    results = cursor.fetchall()
    conn.close()

    if(len(results) == 0):
        return False
    else:
        return True


def db_remove_task(task):
    '''
    :param task: the task we want to remove from the db
    This method remove from the db a specific task
    '''

    # prepare the query text
    sql = "delete from task where todo = ?"

    # connect to the db
    conn = sqlite3.connect("task_list.db")
    cursor = conn.cursor()
    result = -1
    try:
        # execute the query passing the needed parameters
        cursor.execute(sql, (task,))
        # commit all pending executed queries in the connection
        conn.commit()
        result = 1
    except Exception as e:
        print(str(e))
        # if something goes wrong: rollback
        conn.rollback()

    # close the connection
    conn.close()

    return result

def db_remove_multiple_tasks(text):
    '''
    :param text: text (or part of it) of the task we want to remove from the db
    This method remove from the db all the tasks that contain the specified string
    '''

    # prepare the query text
    sql = "delete from task where todo LIKE ?"

    # add percent sign (%) wildcard to select all the strings that contain specified text
    # <<the multiple character percent sign (%) wildcardcan be used to represent any number of characters in a value match>>
    text = "%" + text + "%"

    #connect to the db
    conn = sqlite3.connect("task_list.db")
    cursor = conn.cursor()

    result = -1
    try:
        #execute the query passing the needed parameters
        cursor.execute(sql, (text, ) )
        #commit all pending executed queries in the connection
        conn.commit()
        result = 1
    except Exception as e:
        print(str(e))
        # if something goes wrong: rollback
        conn.rollback()

    #close the connection
    conn.close()

    return result