#!/usr/bin/python
# -*- coding:UTF-8 -*-

import codecs
import logging
import time

import unicodecsv

years = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013"]
fields = ["法人代码", "法人单位", "行政区划代码", "电话号码", "开业时间年", "地", "县", "行业代码", "注册类型", "从业人员总", "从业人员女", "主营业务收入",
          "工业总产值", "新产品产值", "固定资产净值", "负债合计", "利润总额", "研究开发费", "应付职工薪酬", "港澳台资本", "外商资本", "资产总计", "长途区号", "工业增加值"]
keyFields = [["法人代码"], ["法人单位"], ["行政区划代码", "电话号码", "开业时间年"]]

keyFieldsIndex = []

fullData = []

fullMap = {}


def main():
    logging.basicConfig(filename="log"+time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))+".txt", level=logging.DEBUG)
    logger = logging.getLogger("default")
    logger.info('start running')
    init()
    for year in years:
        data = loadCSV(year)
        handleData(year, data)
    output()
    logger.info("finish")


def init():
    logger = logging.getLogger("init")
    logger.info("start init")
    for i, group in enumerate(keyFields):
        indexGroup = []
        for j, key in enumerate(group):
            if not key in fields:
                logger.error("can not found %s in group %s location %s" % (key, i, j))
                continue
            indexGroup.append(fields.index(key))
        if len(indexGroup) > 0:
            keyFieldsIndex.append(indexGroup)
    logger.info("keyFieldsIndex:"+str(keyFieldsIndex))
    logger.info("finish init")


def loadCSV(year):
    logger = logging.getLogger("loadCSV" + str(year))
    logger.info("start")
    with open(str(year)+".csv", "r") as csvfile:
        reader = unicodecsv.reader(
            csvfile, encoding='utf-8-sig', delimiter=',')
        headers = next(reader)
        headMapper = [-1]*len(fields)
        for col, head in enumerate(headers):
            headEncode = head.encode("utf-8")
            if not headEncode in fields:
                logger.warn("missing field %s" % head)
                continue
            headMapper[fields.index(headEncode)] = col
        logger.info("mapper %s" % headMapper)
        data = []
        for row in reader:
            datarow = [""]*len(fields)
            for j, index in enumerate(headMapper):
                if index >= 0:
                    datarow[j] = row[index].encode("utf-8").strip().rstrip().replace('　', '')
            data.append(datarow)
    logger.info("%d row got" % len(data))
    logger.info("finish")
    csvfile.close()
    return data


def handleData(year, data):
    logger = logging.getLogger("handleData" + str(year))
    logger.info("start")
    newCound = 0
    foundCount = 0
    for row in data:
        found = False
        for i, _ in enumerate(keyFieldsIndex):
            key = getMapperKey(i, row)
            if len(key) == 0:
                logger.warn("missing key field %s", formatSlice(keyFields[i]))
                logger.warn(formatRow(row, year))
                continue
            if key in fullMap:
                found = True
                foundCount += 1
                if year in fullData[fullMap[key]]:
                    logger.warn("repeat data found with rull %s" % formatSlice(keyFields[i]))
                    logger.warn("new value %s" % formatRow(row, year))
                    for cyear in years:
                        if cyear in fullData[fullMap[key]]:
                            logger.warn("original value %s" % formatRow(fullData[fullMap[key]][cyear], cyear))
                fullData[fullMap[key]][year] = row
                break
        if not found:
            newCound += 1
            location = len(fullData)
            fullData.append({})
            fullData[location][year] = row
            for i, _ in enumerate(keyFieldsIndex):
                key = getMapperKey(i, row)
                fullMap[key] = location
    logger.info("new %d , found %d" % (newCound, foundCount))
    logger.info("finish")


def output():
    logger = logging.getLogger("output")
    logger.info("output start")
    skip = 0
    with open("out.csv", 'wb') as outfile:
        outfile.write(codecs.BOM_UTF8)
        writer = unicodecsv.writer(outfile, encoding='utf-8-sig')
        writer.writerow(["年"]+fields)
        for entity in fullData:
            if len(entity) < len(years):
                skip += 1
                continue
            for year in years:
                writer.writerow([year] + entity[year])
        outfile.close()
    logger.info("skip %d records" % skip)
    logger.info("output finish")


def getMapperKey(index, row):
    result = str(index)
    for v in keyFieldsIndex[index]:
        result += "-" + str(row[v])
        if len(str(row[v])) == 0:
            return ""
    return result


def formatSlice(s):
    result = "["
    for i in s:
        result += str(i)
        result += ","
    result += "]"
    return result


def formatRow(row, year):
    result = "[年:%s]" % year
    for i, v in enumerate(fields):
        result += ("[%s:%s]" % (v, row[i]))
    return result


if __name__ == '__main__':
    main()
