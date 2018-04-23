from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import db_interaction


def new_task(bot, update, args):
    '''
    Add a new element to the given list
    '''

    # args is a list: when you insert words separated by a space, it considers the space as a separator and creates a list of all the inserted words
    # to re-create the string, you can simply join the words inserting a space among them
    taskToAdd = ' '.join(args)

    if taskToAdd and taskToAdd.strip() and (not taskToAdd.isspace()):

        # insert the task in the db and return a message
        result = db_interaction.db_insert_task(taskToAdd)
        if (result>0):
            message = "The new task was successfully added to the list!"
        else:
            message = "No task was inserted due to a problem! Try again!"
    else:
        message = "You did not specify any task!"
    # send the generated message to the user
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

def remove_task(bot, update, args):
    '''
    Remove an element from the given list
    '''

    # args is a list: when you insert words separated by a space, it considers the space as a separator and creates a list of all the inserted words
    # to re-create the string, you can simply join the words inserting a space among them

    taskToRemove = ' '.join(args)

    message = ''
    if taskToRemove and taskToRemove.strip() and (not taskToRemove.isspace()):

        if(db_interaction.db_contains(taskToRemove)):
            result = db_interaction.db_remove_task(taskToRemove)

            if (result > 0):
                message = "The task was successfully removed!"
            else:
                message = "No task was deleted due to a problem! Try again!"
        else:
            message = "The task you specified is not in the database!"
    else:
        message = "You did not specify any task!"
    #send the generated message to the user
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    # send the updated list as a message
    newMessage = "Now the list contains the following items:"
    bot.sendMessage(chat_id=update.message.chat_id, text=newMessage)
    updatedTaskList = db_interaction.get_sorted_tasks_list()
    bot.sendMessage(chat_id=update.message.chat_id, text=updatedTaskList)

def remove_multiple_tasks(bot, update, args):
    '''
    Remove all the elements that contain a provided string
    '''

    # args is a list: when you insert words separated by a space, it considers the space as a separator and creates a list of all the inserted words
    # to re-create the string, you can simply join the words inserting a space among them
    substring = ' '.join(args)
    message = ''

    if substring and substring.strip() and (not substring.isspace()):
        # substring is not None AND substring is not empty or blank AND substring is not only made by spaces

        result = db_interaction.db_remove_multiple_tasks(substring)

        if (result>0):
            message = "The elements were successfully removed!"
        else:
            message = "No task was deleted due to a problem! Try again!"
    else:
        message = "You did not specify any string!"
    # send the generated message to the user
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    # send the updated list as a message
    newMessage = "Now the list contains the following items:"
    bot.sendMessage(chat_id=update.message.chat_id, text=newMessage)
    updatedTaskList = db_interaction.get_sorted_tasks_list()
    bot.sendMessage(chat_id=update.message.chat_id, text=updatedTaskList)

def print_sorted_list(bot, update):
    '''
    Print the elements of the list, sorted in alphabetic order
    '''
    tasks_list = db_interaction.get_sorted_tasks_list()
    message = ''
    # check if the list is empty
    if (len(tasks_list) == 0):
        message = "Nothing to do, here!"
    else:
        # we don't want to modify the real list of elements: we want only to print it after sorting
        # there are 2 possibilities:
        # a) using the sort method
        #  temp_tasks_list = tasks_list[:]
        #  temp_tasks_list.sort()
        #  message = temp_tasks_list
        # b) using the sorted method (the sorted method returns a new list)
        message = tasks_list
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


# define one command handler. Command handlers usually take the two arguments:
# bot and update.
def start(bot, update):
    update.message.reply_text('Hello! This is AmITaskListBot. You can use one of the following commands:')
    update.message.reply_text('/newTask <task to add>')
    update.message.reply_text('/removeAllTasks <substring used to remove all the tasks that contain it>')
    update.message.reply_text('/showTasks')


def echo(bot, update):
    # get the message from the user
    receivedText = update.message.text
    textToSend = "I'm sorry,. I'm afraid I can't do that"
    bot.sendMessage(chat_id=update.message.chat_id, text=textToSend)

if __name__ == '__main__':
    # main program

    updater = Updater(token='566166482:AAGsEbchP_cr_A6sxRB45cQm5H1O9cJFtB4')

    # add an handler to start the bot replying with the list of available commands
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    # on non-command textual messages - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # add an handler to insert a new task in the list
    newTask_handler = CommandHandler('newTask', new_task, pass_args=True)
    dispatcher.add_handler(newTask_handler)

    # add an handler to remove the first occurence of a specific task
    removeTask_handler = CommandHandler('removeTask', remove_task, pass_args=True)
    dispatcher.add_handler(removeTask_handler)

    # add an handler to remove from the list all the existing tasks that contain a provided string
    removeAllTasks_handler = CommandHandler('removeAllTasks', remove_multiple_tasks, pass_args=True)
    dispatcher.add_handler(removeAllTasks_handler)

    # add an handler to show the list tasks
    showTasks_handler = CommandHandler('showTasks', print_sorted_list)
    dispatcher.add_handler(showTasks_handler)

    # start the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()