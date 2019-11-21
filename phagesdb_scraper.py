import requests
from bs4 import BeautifulSoup
import os.path
import csv

##############################################################################
def getValidFile():
    file = input("Input file name: ")
    print()
    while os.path.isfile(file) == False:
        print("Sorry, that is not a valid file option. Try again. \n")
        file = input("Input file name: ")
        print()
    return file
##############################################################################
def readFile():
    fileName = getValidFile()

    info = open(fileName)
    rawData = info.read()

    dataList = rawData.split("\n")

    info.close()
    return dataList
##############################################################################
def createLinks(phages):
        links = []
        for phage in phages:
            link = "https://phagesdb.org/phages/" + phage.strip() + "/"
            links.append(link)
        return links
##############################################################################
def getPhageData(phage, link):
    dataRow = []
    phage = phages[i]

    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    labels = soup.select("td.detailLabel")
    values = soup.select("td.detailValue")

    host = "--"
    location = "--"
    genomeLength = "--"
    genomeEnd = "--"
    gc = "--"
    cluster = "--"
    subcluster = "--"
    life = "--"
    type = "--"

    for j in range(len(labels)):
        if labels[j].text == "Isolation Host":
            host = values[j].select("em")[0].text
        if labels[j].text == "Location Found":
            location = values[j].text
        if labels[j].text == "Genome length (bp)":
            genomeLength = values[j].text
        if labels[j].text == "Character of genome ends":
            genomeEnd = values[j].text
        if labels[j].text == "GC Content":
            raw = values[j].text
            gc = raw[:len(raw) - 1]
        if labels[j].text == "Cluster":
            cluster = values[j].text
        if labels[j].text == "Subcluster":
            subcluster = values[j].text
        if labels[j].text == "Cluster Life Cycle":
            life = values[j].text
        if labels[j].text == "Morphotype":
            type = values[j].text

    dataRow.append(phage)
    dataRow.append(host)
    dataRow.append(location)
    dataRow.append(genomeLength)
    dataRow.append(genomeEnd)
    dataRow.append(gc)
    dataRow.append(cluster)
    dataRow.append(subcluster)
    dataRow.append(life)
    dataRow.append(type)

    return dataRow
##############################################################################
def makeCSV(data):
    with open("phageData.csv","w+") as phageData:
        csvWriter = csv.writer(phageData, delimiter=',')
        csvWriter.writerows(data)
    phageData.close()
##############################################################################
if __name__ == '__main__':
    phages = readFile()
    links = createLinks(phages)
    data = [["Name", "Isolation Host", "Location Found", \
            "Genome length (bp)", "Character of genome ends", "GC Content", \
            "Cluster", "Subcluster", "Cluster Life Cycle", "Morphotype"]]
    for i in range(len(phages)):
        phage = phages[i]
        link = links[i]
        row = getPhageData(phage, link)
        data.append(row)
        print(row)
    makeCSV(data)
