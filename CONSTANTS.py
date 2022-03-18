'''
    You can define some constants in this file,
    including but not limited to 
    1. Networking protocol field code
    e.g., REQUEST = 0, REPLY = 1 ...
    2. Other constant parameteres
'''

# Here we define the constants for CIL menu
# MENU
import pyaudio

MAIN = 1
MEETING = 2

# Server ports
XXPORT = 1111
YYPORT = 1112
ZZPORT = 1113
AAPORT = 1114

CHUNK = 1024
FORMAT = pyaudio.paInt16    # 格式
CHANNELS = 2    # 输入/输出通道数
RATE = 44100    # 音频数据的采样频率
RECORD_SECONDS = 0.5    # 记录秒