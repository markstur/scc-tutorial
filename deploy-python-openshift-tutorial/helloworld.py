import os
import logging
import subprocess

from flask import Flask

TEST_FILE = "/var/opt/app-root/src/data/testfile.txt"
INFO = logging.INFO
ERROR = logging.ERROR
DEBUG = logging.DEBUG
BULLETS = {
    INFO: ' *** ',
    ERROR: '!!! ',
    DEBUG: ' '
}
TAGS = {
    INFO: 'code style="color:green;"',
    ERROR: 'b style="color:red;"',
    DEBUG: 'small'
}

logging.basicConfig(level=logging.INFO)

application = Flask(__name__)


def tests():

    msgs = ["<h1>Testing for expected security context</h1>"]

    def msg(level, message):

        b = BULLETS[level]
        t = TAGS[level]
        application.logger.log(level, f' {b} {message} {b}')
        msgs.append(f"<{t}>{message}</{t}><br/>")

    # Test: Who am I?
    msgs.append("<h3>User ID Testing</h3>")
    expected_uid = 1234
    msg(INFO, f"This app expects to run with user ID = {expected_uid}")
    uid = os.getuid()
    gid = os.getgid()
    msg(INFO, f"Actual user ID = {uid}")
    msg(DEBUG, f"Actual group ID = {gid}")
    try:
        assert uid == expected_uid, f"UID {uid} != {expected_uid}"
        msg(INFO, "SUCCESS: Running as the expected user ID")
    except Exception as e:
        msg(ERROR, repr(e))

    # Test: SYS_TIME
    msgs.append("<h3>SYS_TIME Testing</h3>")
    out = subprocess.run(["date", "-s", "00:00:00"],
                         stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    print(out)
    msg(INFO, f"Set time returncode: {out.returncode}")
    msg(INFO, f"Set time stdout: {out.stdout}")
    msg(INFO, f"Set time stderr: {out.stderr}")
    try:
        assert 0 == out.returncode, f"returncode != 0"
        assert b'' == out.stderr, f"stderr != empty"
        msg(INFO, "SUCCESS: Set time returncode and stderr OK")
    except Exception as e:
        msg(ERROR, repr(e))

    msgs.append("<h3>File Write Testing</h3>")
    msg(INFO, f"This app expects to write a file in {TEST_FILE}")
    msg(INFO, "Write to a file and read it back.")
    try:
        w = "Look at this. I wrote to a file."
        f = open(TEST_FILE, "w")
        f.write(w)
        f.close()
        msg(INFO, f"Wrote to file: {w}")
        f = open(TEST_FILE, "r")
        r = f.read()
        f.close()
        msg(INFO, f"Read back: {r}")
        assert r == w, f"Wrote:{w} != Read:{r}"
    except Exception as e:
        msg(ERROR, repr(e))

    msgs.append("<h3>File user/group Testing</h3>")
    try:
        msg(INFO, f"Test file name: {TEST_FILE}")
        msg(INFO, f"Test file owner: {os.stat(TEST_FILE).st_uid}")
        msg(INFO, f"Test file group: {os.stat(TEST_FILE).st_gid}")
        msg(INFO, f"os.chown {TEST_FILE} -1:5656")
        os.chown(TEST_FILE, -1, 5656)
        msg(INFO, f"st_uid: {os.stat(TEST_FILE).st_uid}")
        msg(INFO, f"st_gid: {os.stat(TEST_FILE).st_gid}")
        os.chown(TEST_FILE, uid, gid)
        msg(INFO, f"os.chown {TEST_FILE}, {uid}, {gid}")
        msg(INFO, f"st_uid: {os.stat(TEST_FILE).st_uid}")
        msg(INFO, f"st_gid: {os.stat(TEST_FILE).st_gid}")
    except Exception as e:
        msg(ERROR, repr(e))

    # For pod log print all the messages one at a time
    # for m in msgs:
        # application.logger.log(INFO, m)

    # Return the messages "formatted" for the web page
    return ''.join(msgs)


@application.route('/')
def hello():
    return tests()


if __name__ == '__main__':
    application.run()
