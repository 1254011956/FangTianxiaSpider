# -*- coding: utf-8 -*-
# @Time : 2020/5/15 10:52 
# @Author : 永
# @File : text.py 
# @Software: PyCharm

import re

li = ['\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '/\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t－\n\t\t\t\t\t\t\t\t\t\t\t\t337~375平米\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t']

area = re.sub(r"[\W*\\a-z]","",str(li))

print(area)