name = None
surname = None
age = None
sex = None

def set_name(user_name : str):
    global name

    name = user_name

    assert len(name) > 0, "This isn't a valid name"

def set_surname(user_surname : str):
    global surname

    surname = user_surname

    assert (len(surname) > 0), "This isn't a valid surname"

def set_age(user_age : int):
    global age

    age = user_age

    assert (age > 0), "This isn't a valid age"

def set_sex(user_sex : str):
    global sex

    sex = user_sex

    assert (sex == "male" or sex == "female"), "This isn't a valid sex"

def commander(command,arg,message):
    assert command(arg), message

def perform(f):
    f()

sex = "male"

commander(lambda a: (a == "male" or a == "female"),sex,"Error message")

perform(lambda: set_name("giorgos"))
perform(lambda: set_surname("Tziokas"))
perform(lambda: set_age(27))
perform(lambda: set_sex("male"))

