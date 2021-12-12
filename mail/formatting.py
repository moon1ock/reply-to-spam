



msg_template = """Dear {name},

I got your time wasted!

Yours sincerely,
Ron Obvious"""

def format_msg(my_name="Andriy"):
    my_msg = msg_template.format(name=my_name)
    return my_msg