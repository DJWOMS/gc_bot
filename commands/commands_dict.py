from commands import *


light_commands = {
    '!paste': share_code,
    '!web': search_web,
    '!tut': django_tutorials,
    '!wq': wide_question,
    '!flood': flood,
}


sudo_commands = {
    '!ban': ban_user,
    '!warn': warn_user,
    '!sudo': add_sudo_user,
    '!unban': unban_user,
}