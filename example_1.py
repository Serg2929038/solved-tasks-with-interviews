# -*- coding: utf-8 -*-
"""Задача 1
Дан файл, содержащий текстовую строку – указание пути к дисковому устройству в системе Linux. Прочитайте файл и выведите на экран (stdout) следующую информацию о дисковом устройстве:
    • Тип устройства, например: disk, part, lvm, rom;
    • Общий объем в гигабайтах;
    • выведите также:
     ◦ Объём свободного пространства в мегабайтах;
    ◦ Тип файловой системы, например: ext4, swap;
На Linux-системе, где будет исполняться код, установлены пакеты coreutils и util-linux.
Пример 1:
Входной файл:
	/dev/sda
Вывод:
	/dev/sda disk 64G
Пример 2:
Входной файл:
	/dev/sda1
Вывод:
	/dev/sda1 part 1G 238M ext2 /boot"""

###### Решение #####
import os
from pathlib import Path
import psutil

def open_f(path):
    with open(path) as f:
        line = f.readline()
        return line

def get_parti(path):
    line = open_f(path)
    partitions = psutil.disk_partitions(all=False)
    for i in partitions:
        if i.device == line:
            return ("device= {}".format(i.device), 'mountpoint={}'.format(i.mountpoint), 'fstype={}'.format(i.fstype))
    return None

def get_fs_type(path):
    mypath = open_f(path)
    root_type = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            root_type = part.fstype
            continue
        if mypath.startswith(part.mountpoint):
            return part.fstype
    return root_type

def size_dir(path):
    root_directory = Path(open_f(path))
    # root_directory = Path(path)
    summ = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    if int(summ/1024**3) == 0:
        return ('Drictory size: {} MB'.format(int(summ/1024**2)))
    elif int(summ%1024**3) != 0 and int(summ//1024**3) != 0:
        gb= summ/1024**3
        mb = summ%1024**3
        if (mb/1024**2) > 1000:
            gb += (mb/1024**2)//1000
            mb =(mb/1024**2)%1000
        return ('Drictory size: {} GB {} MB'.format(int(gb),int(mb)))
    return ('Drictory size: {:,} GB'.format(int(summ/1024**3)).replace(',', ' '))

# /dev/sda7
if __name__ == '__main__':
    path = os.getcwd()+ '/file_17_12_2019'
    print(open_f(path), end=' ')
    print(get_fs_type(path), end=' ')
    print(size_dir(path), end=' ')