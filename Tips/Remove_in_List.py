# ループ内でリストの要素を削除する時の注意


data1 = [1, 2, 3, 4, 5]
for i in data:
    data1.remove(i)

print(data1)

'''
結果
data1 = [2, 4]
となる。
これはリスト内で要素を削除すると次の要素が飛ばされてしまう仕様である。
'''

data2 = [1, 2, 3, 4, 5]
for i in data[:]:
    data.remove(i)

print(data2)

'''
結果
data2 = []
想定どおり。
データを取り出したいだけであれば
removeより内包表記を使う方が速度も有利で
バグも生まれにくい。
'''
