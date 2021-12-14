classes_dict = {}


classes_dict["gold scam"] = {}
classes_dict["gold scam"]["pattern"] = ["I am prince africa", "send gold", "metric tons gold"]
classes_dict["gold scam"]["response"] = ['I am very interested! What quantities of gold are we talking about?',\
'Wow, I am not sure if this email was meant for me. Just to check, was the gold organically mined? I sure hope no childred suffered during the process!']


classes_dict["unsure"] = {}
classes_dict["unsure"]["pattern"] = [""]
classes_dict["unsure"]["response"] = ['Hey, sorry! I was very busy having a trivia night at my elderly home! So I lost track of what was the issue. By the way, do you know what\'s the biggest continent in the world?']
