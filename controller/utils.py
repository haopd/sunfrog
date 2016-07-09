# -*- coding: utf-8 -*-
import logging
import random
import re
import hashlib
import hmac
import string
import datetime
import urlparse

import webapp2

__author__ = 'tarzan'
_logger = logging.getLogger(__name__)


_phone_re = re.compile(r'^(?:84|0)?(9\d{8}|1\d{9}|8\d{8}|10000\d{4})$', re.S)
_phone_normalize_re = re.compile(r'[+\-()\[\]|\s:]')
_internal_phone_re = re.compile(r'^\+(?:84|0)?(10000\d{4})$', re.S)

sure_unicode = lambda s: s if isinstance(s, unicode) else s.encode('utf-8')
sure_str = lambda s: s if isinstance(s, str) else s.encode('utf-8')


def normalize_phone_number(num):
    """ Chuẩn hóa 1 số điện thoại, đưa về dang chuẩn quốc tế +84...

    Args:
        num (str): số điện thoại cần chuẩn hóa

    Returns:
        str: số điện thoại đã được chuẩn hóa

        Hoặc None nếu không thể chuẩn hóa

    >>> normalize_phone_number('0985501504')
    '+84985501504'
    >>> normalize_phone_number('(+84) 985 501 504')
    '+84985501504'
    >>> normalize_phone_number('0985-501-5 04  ')
    '+84985501504'
    >>> normalize_phone_number('0 10000 4333')
    '+84100004333'
    """
    num = _phone_normalize_re.sub('', num)
    m = _phone_re.match(num)
    if m:
        return '+84' + m.groups()[0]
    return '+84' + num if _phone_re.match(num) else None


def normalize_email(email):
    """ Chuẩn hóa 1 địa chỉ email. Địa chỉ email sẽ được đưa về dạng lower, rồi
    kiểm tra định dạng xem đúng hay không.
    Args:
        email (str): địa chỉ email cần chuẩn hóa

    Returns:
        str: Địa chỉ email đã chuẩn hóa.

        None nếu email không đúng.

    >>> normalize_email('HOC3010@gmail.COM')
    'hoc3010@gmail.com'
    >>> normalize_email('not an email@domain.com')
    >>> normalize_email('not_an_email@domain.com')
    'not_an_email@domain.com'
    >>> normalize_email('not_an_email')
    """
    is_email = validate_email(email)
    return email.lower() if is_email else None


def normalize_fullname(fullname):
    """ Chuẩn hóa, tách tên đầy đủ thành first_name và last_name

    Args:
        fullname (unicode): tên đầy đủ

    Returns:
        (unicode, unicode): (first_name, last_name)

    """
    fullname = fullname.strip()
    words = [w.capitalize() for w in fullname.split()]
    count = len(words)

    if not words:
        return (u'', u'')

    first_name_length = 2 if count >= 3 else 1

    first_name = u' '.join(words[0:first_name_length])
    last_name = u' '.join(words[first_name_length:])

    return [first_name, last_name]


def hash_password(password, salt):
    """ Băm mật khẩu để so sánh sau này.
    Thuật toán sử dụng là HMAC với SHA1

    Args:
        password (str): mật khẩu cần băm
        salt (str): mã gây nhiễu

    Returns:
        str: giá trị băm của mật khẩu

    >>> hash_password("The quick brown fox jumps over the lazy dog", "key")
    'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9'
    """
    if not password or not salt:
        return None
    salt = sure_str(salt)
    password = sure_str(password)

    hashed = hmac.new(salt, password, hashlib.sha1)
    return sure_unicode(hashed.hexdigest())


def is_password_match(password, hash, salt):
    """ Kiểm tra xem password có đúng với mã băm password hay không?
    Args:
        password (str): password cần kiểm tra
        hash (str): Mã băm password. Xem :func:`.hash_password`
        salt (str): xâu gây nhiễu. Xem :func:`.hash_password`

    Returns:
        bool: Password có đúng hay không?
    >>> is_password_match("The quick brown fox jumps over the lazy dog", "de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9", "key")
    True
    >>> is_password_match("The quick brown fox jumps over the lazy dog", "df7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9", "key")
    False
    >>> is_password_match("heineken", "0106a7e14856bbdc8919f8b44457050544e3470a", "iZ7Tjs")
    False
    """
    return password and salt and (hash == hash_password(password, salt))


def random_string(length=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))


def random_digits(length=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(length))


def datetime_2_timestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return int((td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6)


def convert_md5(str,checksum):
    """
    mã hoá md5 cho tất cả password
    :param str: chuỗi cần mã hoá
    :param checksum: chuỗi gây nhiễu
    :return: trả về chuỗi đã mã hoá md5

    >>> convert_md5('Hello world!','aDf5ma')
    '2ccf0f5a067e272a007382fe7103a582'
    >>> convert_md5('Hello world!','')
    '86fb269d190d2c85f6e0468ceca42a20'
    """
    m = hashlib.md5()
    m.update(str)
    m.update(checksum)
    value = m.hexdigest()
    return value


