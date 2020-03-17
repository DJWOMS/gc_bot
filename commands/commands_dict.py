"""Light commands available to all users. But sudo only admin or sudoers"""

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
    '!sudo': sudo_add_user,
    '!unban': unban_user,
}