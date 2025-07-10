import requests
from bs4 import BeautifulSoup
import re
import xlwt

# 正则表达式
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

def geturl(url):
    head = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=head)
        return response.text
    except:
        return ""

def getdata(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = geturl(url)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        for item_tag in soup.find_all("div", class_='item'):
            data = []
            item_str = str(item_tag)
            data.append(re.findall(findLink, item_str)[0] if re.findall(findLink, item_str) else " ")
            data.append(re.findall(findImgSrc, item_str)[0] if re.findall(findImgSrc, item_str) else " ")
            titles = re.findall(findTitle, item_str)
            if len(titles) == 2:
                data += [titles[0], titles[1].replace("/", "")]
            elif len(titles) == 1:
                data += [titles[0], " "]
            else:
                data += [" ", " "]
            data.append(re.findall(findRating, item_str)[0] if re.findall(findRating, item_str) else " ")
            data.append(re.findall(findJudge, item_str)[0] if re.findall(findJudge, item_str) else " ")
            inq = re.findall(findInq, item_str)
            data.append(inq[0].replace("。", "") if inq else " ")
            bd_match = re.findall(findBd, item_str)
            if bd_match:
                bd = re.sub(r'<br(\s+)?/>(\s+)?', " ", bd_match[0])
                bd = re.sub(r'/', " ", bd)
                data.append(bd.strip())
            else:
                data.append(" ")
            if len(data) == 8:
                datalist.append(data)
    return datalist

def savedata(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet("豆瓣电影top250", cell_overwrite_ok=True)
    column = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        worksheet.write(0, i, column[i])
    for i, data in enumerate(datalist):
        if len(data) == 8:
            for j in range(0, 8):
                worksheet.write(i + 1, j, data[j])
    workbook.save(savepath)
