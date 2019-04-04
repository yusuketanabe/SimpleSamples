#!/usr/bin/env python

from threading import Thread, Lock, Event
import random
import time


# ブロック付きキュー BlockingQueueはPython標準モジュールのqueueで実現できる。
class BlockingQueue(object):

    def __init__(self):
        self.queue = []
        self.lock = Lock()
        self.event = Event()

    def push(self, obj):
        # ロックを取得する
        with self.lock:
            # キューに要素を追加する
            self.queue.append(obj)
            # キューに要素を追加したことをwait()でブロックしている別のスレッドに通知する
            self.event.set()

    # 2.Lockを保持したままwait()しているのでデッドロック（２つ以上のスレッドあるいは
    # プロセスなどの処理単位が互いの処理終了を待ち、結果としてどの処理も先に進めなく
    # なってしまうことを言う）状態になるバグあり
    '''
    def pop(self):
        # waitを抜けたスレッドが復帰するループ
        while True:
            # ロックを取得する
            with self.lock:
                if self.queue:
                    # キューに要素があればそれを返す
                    return self.queue.pop()
                else:
                    # 1.追加し実行するとwaiting...が大量表示でwait()スレッドが待機していないことがわかる
                    # これはclear()を呼んでいないために一度set()を呼び出した後はwait()を呼び出しても待機しないから
                    print("waiting...")
                    # キューが空なら別のスレッドが要素を追加して通知してくるまで待つ
                    self.event.wait()
    '''

    # 3.修正版
    def pop(self):
        # waitを抜けたスレッドが復帰するループ
        while True:
            self.event.clear()
            # ロックを取得する
            with self.lock:
                if self.queue:
                    # キューに要素があればそれを返す
                    return self.queue.pop()
            print("waiting ...")
            # キューが空なら別のスレッドが要素を追加して通知してくるまで待つ
            self.event.wait()


# キューから要素を取得するスレッド
class Consumer(Thread):

    def __init__(self, queue):
        # super(Consumer, self).__init__() 第一引数に自クラス、第二引数にインスタンス
        super().__init__()  # Python3では引数を省略できる
        # daemonとはバックグラウンドプロセス
        # daemon=Trueでスレッドをdaemon化。デフォルトはFalse。
        # 指定がない場合はスレッドを生成したスレッドの状態を継承する
        # デーモンスレッドはスレッドがデーモンスレッドのみになった時に自動的にプログラムを終了する。
        # これはデーモンスレッドが破棄されるため。
        self.daemon = True
        self.queue = queue

    def run(self):
        while True:
            # キューから要素を取り出しては標準出力にプリントする
            print(self.queue.pop())


# キューに要素を追加するスレッド
class Producer(Thread):

    def __init__(self, queue):
        # super(Producer, self).__init__()
        super().__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        while True:
            # 1秒ごとにランダムな数値をキューに追加する
            self.queue.push(random.randint(0, 256))
            time.sleep(1)


if __name__ == '__main__':
    # 複数のスレッドから共有されるキュー
    q = BlockingQueue()
    # キューに要素を追加するスレッド
    p = Producer(q)
    # キューから要素を取得するスレッド
    c = Consumer(q)
    p.start()
    c.start()

    # mainスレッドを1秒間隔で無限ループさせる
    while True:
        time.sleep(1)
