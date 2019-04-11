import fcntl

i2c_lock_fd = None

def i2c_lock():
    global i2c_lock_fd
    try:
        #print("Trying lock...")
        i2c_lock_fd = open('/tmp/i2c.lock', 'w')
        fcntl.lockf(i2c_lock_fd, fcntl.LOCK_EX)
        #print("Acquired lock...")
    except:
        raise

def i2c_unlock():
    global i2c_lock_fd
    try:
        if not i2c_lock_fd:
            return False
        fcntl.lockf(i2c_lock_fd, fcntl.LOCK_UN)
        i2c_lock_fd.close()
        i2c_lock_fd = None
        #print("Unlocked.")
    except:
        raise
    return True
