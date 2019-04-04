def gcd(x, y):
    """
    gsd: greatest common divisor
    最大公約数
    mathモジュールにgcd()関数あるけどね。
    ユークリッドの互除法: x, yのうち大きい数を小さい数で割り、余りが出る。
    更に先ほど割った数を、出た余りで割る。余りが0になるまで続けて、最後に割った数が
    最大公約数である。
    下のコードについて: while y は y == 1(True) の時にループ。0(False) になると
    ループから出る。y はループ２週目から余りになる。
    x, y = y, x % y は x と y を入れ替える。gcd(大, 小) で入力されたらそのまま
    計算されるが、gcd(小, 大) で入力されたら、例えば (x, y) = (18, 24) なら
    x, y = y, x % y で x = 24, y = 18 % 24 = 18 となり入れ替わる。
    最終的に x が最大公約数として返される。
    """
    while y:
        x, y = y, x % y
    return x


def lcm(p, q):
    """
    lcm: least common multiple
    最小公倍数を求める関数
    """
    return (p * q) // gcd(p, q)


def generate_keys(p, q):
    """
    与えられた２つの素数p, qから秘密鍵と公開鍵を生成する。
    """
    N = p * q
    L = lcm(p-1, q-1)

    for i in range(2, L):
        # p と q の最小公倍数と互いに素になる整数 i を探して E（公開鍵）とする
        if gcd(i, L) == 1:
            E = i
            break

    for i in range(2, L):
        # 秘密鍵の条件、秘密鍵 * 公開鍵 = L * n + 1 になる数を探す
        if (E * i) % L == 1:
            D = i
            break
    # (E, N)が公開鍵、(D, N)が秘密鍵
    return (E, N), (D, N)


def encrypt(plain_text, public_key):
    """
    公開鍵 public_key を使って平文 plain_text を暗号化する
    ord(): 文字のUnicodeポイントコードを表す整数を返す
    pow(x, y, z): xのy乗を返す。zがあれば、xのy乗に対するzの剰余を返す。x**y mod z
    pow(x, y) % zより効率的。pow(x, y)はx**yと同等。
    """
    E, N = public_key
    plain_integers = [ord(char) for char in plain_text]
    encrypted_integers = [pow(i, E, N) for i in plain_integers]
    encrypted_text = ''.join(chr(i) for i in encrypted_integers)

    return encrypted_text


def decrypt(encrypted_text, private_key):
    """
    秘密鍵 private_key を使って暗号文 encrypted_text を復号化する
    """
    D, N = private_key
    encrypted_integers = [ord(char) for char in encrypted_text]
    decrypted_integers = [pow(i, D, N) for i in encrypted_integers]
    decrypted_text = ''.join(chr(i) for i in decrypted_integers)

    return decrypted_text


def sanitaize(encrypted_text):
    """
    UnicodeEncodeError が起きないようにする。
    """
    return encrypted_text.encode('utf-8', 'replace').decode('utf-8')

if __name__ == '__main__':
    public_key, private_key = generate_keys(101, 3259)

    plain_text = 'テスト、テスト。RSAのテストー。この文章がちゃんと見えますか？'
    encrypted_text = encrypt(plain_text, public_key)
    decrypted_text = decrypt(encrypted_text, private_key)

    print(f'''
    秘密鍵: {private_key}
    公開鍵: {public_key}

    平文: 「{plain_text}」

    暗号文: 「{sanitaize(encrypted_text)}」

    平文（復号化後）: 「{decrypted_text}」
    '''[1:-1])
