



# msg_template = """Dear {name},

# I got your time wasted!

# Yours sincerely,
# Ron Obvious"""

def format_msg(my_name="Andriy", text=""):
    import random
    replies = ['Yours sincerely', 'Best regards,', "Can't wait for your reply!",'All the best!', 'Faithfully yours,']

    my_msg = "Dear "+my_name+",\n\n" +text + '\n\n' + random.choice(replies)+'\nRon Obvious'
    # msg_template.format(name=my_name)
    return my_msg