import bot_vars

def catch_invalid_login_id(user):
    try:
        return str(user.login_id)      
    except AttributeError:
        pass

def catch_invalid_login_name(user):
    try:
        
        username = str(user.name)
        first_last = username.split()
        username = first_last[0]+' '+first_last[-1]
        return username
    except AttributeError:
        pass

def get_student_names():
    print('grabbing student names...')
    course = bot_vars.canvas.get_course(bot_vars.CONST_COSC102_COURSE_ID)
    users = {catch_invalid_login_id(user): catch_invalid_login_name(user) for user in course.get_users()} 
    return users