from enum import Enum

class FriendRequestStatus(Enum):
    NO_REQUEST_SEND = -1
    THEM_SEND_TO_YOU = 0
    YOU_SEND_TO_THEM = 1
