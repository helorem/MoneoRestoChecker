import threading
import Queue
import sqlite3

SQLITE_FILE = "moneoresto-checker.db"

class DBConsumer:
    def __init__(self, filename):
        self.filename = filename
        self.looping = False
        self.queue = Queue.Queue()
        self.thread = threading.Thread(None, self.__loop)
        self.thread.start()
        self.result = None
        self.success = False

    def __loop(self):
        self.db = sqlite3.connect(SQLITE_FILE)
        self.db.row_factory = sqlite3.Row
        self.cur = self.db.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")
        try:
            self.looping = True
            while self.looping:
                try:
                    req, params, commit, evt1, evt2 = self.queue.get(True, 0.1)
                    try:
                        if params:
                            self.cur.execute(req, params)
                        else:
                            self.cur.execute(req)
                        if commit:
                            self.db.commit()
                        self.result = self.cur.fetchall()
                        self.success = True
                    except BaseException as ex:
                        self.success = False
                        self.result = ex
                    evt1.set()
                    evt2.wait(0.1)
                except Queue.Empty:
                    pass
        finally:
            self.db.close()

    def close(self):
        self.looping = False
        self.thread.join(5)

    def query(self, req, params=None, commit=False):
        evt1 = threading.Event()
        evt2 = threading.Event()
        res = self.queue.put_nowait((req, params, commit, evt1, evt2))
        evt1.wait()
        res = self.result
        success = self.success
        evt2.set()
        if not success:
            raise self.result
        return res

    def execute(self, req, params=None):
        self.query(req, params, True)

    instance = None
    @staticmethod
    def get_instance():
        if not DBConsumer.instance:
            DBConsumer.instance = DBConsumer(SQLITE_FILE)
        return DBConsumer.instance



