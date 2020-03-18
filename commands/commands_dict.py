"""Light commands available to all users. But sudo only admin or sudoers"""

from commands import *


light_commands = {
    '!paste': share_process,
    '!web': web_process,
    '!tut': tut_process,
    '!wq': wq_process,
    '!flood': flood_process,
}


sudo_commands = {
    '!ban': ban_process,
    '!warn': warn_process,
    '!sudo': sudo_process,
    '!unban': unban_process,
}