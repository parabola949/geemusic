from geemusic import app
import os
import ctypes



if __name__ == '__main__':
    if ctypes.windll.shell32.IsUserAnAdmin():
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        print('NO ADMIN')