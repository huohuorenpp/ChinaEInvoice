#!/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import io
from PIL import Image as PI
from PIL import ImageFilter
from wand.image import Image
from pyzbar.pyzbar import decode

basedir = os.path.abspath(os.path.dirname(__file__))

def get_qrcode(path):
    file_path = path
    with Image(filename=file_path, resolution=300) as img:
        img.crop(0,0,int(img.width/4),int(img.height/4))
        raw = img.make_blob("png")
        image = PI.open(io.BytesIO(raw)).convert("RGBA")
        try:
            x,y = image.size
            p = PI.new('RGB', image.size, (255,255,255))
            p.paste(image,image)
            return bytes.decode(decode(p)[0][0])
        except:
            return bytes.decode(decode(image)[0][0])

def get_p_qrcode(path):
    file_path = path
    try:
        with PI.open(file_path) as p:
            p = p.crop((0, 0, int(p.width/4), int(p.height/4)))
            raw = p.filter(ImageFilter.DETAIL).convert('L')
            return bytes.decode(decode(raw)[0][0])
    except Exception as ex:
        return ''



def parse_info(str):
    info_list = str.split(",")
    out = {}
    out["receipt_code"] = info_list[2]
    out["receipt_number"] = info_list[3]
    out["receipt_cost"] = info_list[4]
    out["receipt_datetime"] = info_list[5]
    out["receipt_check_code"] = info_list[6]
    return out

#data_header = ["发票代码","发票号码","金额","开票日期","校验码"]



def getinfo(userid,filename):
    row = []
    filepath = os.path.join(basedir, "static","files",str(userid), filename)
    try:
        if filename.endswith('.pdf'):
            item=get_qrcode(filepath)
        else:
            item=get_p_qrcode(filepath)
        info = parse_info(item)
        #row.append(filename)
        row.append(info["receipt_code"])
        row.append(info["receipt_number"])
        row.append(info["receipt_cost"])
        row.append(info["receipt_datetime"])
        row.append(info["receipt_check_code"])
    except:
        #row.append(filename)
        #row.append("未找到二维码信息")
        row.append('')
        row.append('')
        row.append('')
        row.append('')
        row.append('')
    return row

#print(get_p_qrcode('D:\\Project\\Ei\\app\\static\\files\\600116\\01100160011146321481.png'))