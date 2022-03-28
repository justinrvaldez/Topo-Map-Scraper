import os
import time
import glob
import shutil
import zipfile
import PyPDF2
import img2pdf

from selenium import webdriver
from selenium.webdriver.common.by import By
from File_management import move_files
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

# Coordinates: Decimal degrees
LATITUDE, LONGITUDE = '35.341701', '-106.521636'
coordinates = LATITUDE + ', ' + LONGITUDE

# File directories
PROJECT_NAME, DOWNLOAD_DIR = "ProjectName", "C:\\Users\\justi\\Downloads"
PROJECT_DIR = "C:\\Users\\justi\\PythonScrips\\Python_Programming\\PersonalCode\\TopoMaps\\" + PROJECT_NAME

# Create Chrome instance/get USGS Website
topoView = 'https://ngmdb.usgs.gov/topoview/viewer/#4/39.98/-99.93'  # URL for USGS GIS historical topo map database
driver = webdriver.Chrome()
driver.get(topoView)
time.sleep(4)  # Needed for site to load properly

# Locate search-bar element/input coordinates/start search
search_bar = driver.find_element(By.XPATH, '//*[@id="searchInput"]/div[2]/form/input')
search_bar.send_keys(coordinates)
search = driver.find_element(By.XPATH, '//*[@id="searchInput"]/div[2]/button[1]')
search.click()
time.sleep(1)

# # Find number of maps and create a reversed list index
number_of_maps = driver.find_element(By.XPATH, '//*[@id="sideToggle"]/span').text  # Number of maps for coordinates
li = []

for map_num in range(int(number_of_maps)):
    map_num += 1
    li.append(map_num)
li.reverse()  # Reversing the index solves bugs by downloading from newest to oldest

for i in range(int(number_of_maps)):
    xpath_banner = f"//*[@id='recordsTable']/li[{li[i]}]/a"
    xpath_map = f"//*[@id='recordsTable']/li[{li[i]}]/a/span/span[2]/span[6]/span[1]"
    # Expand banner element
    dropdown_element = driver.find_element(By.XPATH, xpath_banner)
    dropdown_element.click()
    # Click map element
    map_element = driver.find_element(By.XPATH, xpath_map)  # Chooses .jpeg element but .KMZ could be useful
    map_element.click()
    time.sleep(1)  # Allow time to load. Any shorter and you get duplicates

# Separate module
move_files(DOWNLOAD_DIR, PROJECT_DIR)
os.chdir(PROJECT_DIR)

# Removes the duplicate years that were not needed for ESA report
# OPTIONAL
# extension = ".zip"
# map_list = []
# for moved_files in glob.glob("*_jpg*.zip"):
#     file_split = moved_files.split('_')
#     if len(file_split) > 6:
#         del file_split[1]
#         del file_split[1]
#         del file_split[2]
#         del file_split[2]
#         new = '_'.join(file_split)
#         if new in map_list:
#             os.remove(moved_files)
#             continue
#         else:
#             map_list.append(new)
#         os.rename(moved_files, new)
#     elif len(file_split) <= 6:
#         del file_split[1]
#         del file_split[2]
#         del file_split[2]
#         new2 = '_'.join(file_split)
#         map_list.append(new2)
#         os.rename(moved_files, new2)

# unzips, extracts, and deletes zip files

# Unzip all files/delete zips

# Unzips files
files_extension = ".zip"
for zips in os.listdir(PROJECT_DIR):  # loop through items in dir
    if zips.endswith(files_extension):  # check for ".zip" extension
        file_name = os.path.abspath(zips)  # get full path of files
        zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
        zip_ref.extractall(PROJECT_DIR)  # extract file to dir
        zip_ref.close()  # close file
        os.remove(file_name)

# Create pdfs from the images
for i in os.listdir(PROJECT_DIR):
    image_path = PROJECT_DIR + '\\' + i
    pdf_path = (PROJECT_DIR + '\\' + i + '_file.pdf')
    image = Image.open(image_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    test = file.write(pdf_bytes)
    image.close()
    file.close()
    os.remove(image_path)

pdf_list = []
for j in glob.glob("*file*.pdf"):
    pdf_list.append(j)

print(pdf_list)

merger = PdfFileMerger()
for pdf in pdf_list:
    merger.append(pdf)

pdf_name = PROJECT_DIR + ".pdf"
merger.write(pdf_name)
merger.close()

# OPTIONAL: Image resize
# # for b in test_list:
# #     os.remove(a)
#
# # Create/read/writer a pdf object
# pdfFileObj = open(pdf_name, 'rb')
#
# pages_count = PdfFileReader(pdfFileObj)
# total_pages = pages_count.getNumPages()
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#
# writerObj = PdfFileWriter()
# number = 1
# for j in range(total_pages):
#     page = pdfReader.getPage(j)
#     page.scaleTo(612, 792)
#     writerObj.addPage(page)
#     outstream = open(PROJECT_DIR + '_final' + '.pdf', 'wb')
#     writerObj.write(outstream)
#     outstream.close()
#     number += 1
# pdfFileObj.close()
# # os.remove('C:\\Users\\justi\\PythonScrips\\Python_Programming\\PersonalCode\\TopoMaps\DaySchool\\test.pdf')
# print('Done')
