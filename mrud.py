from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import csv

# Function Whate of Load Table 100%
def Whating (id,val,mode):
    while 1 :
        if mode == True:
            if( str(val) == driver.find_element_by_id(id).get_attribute("value") ):
                print(driver.find_element_by_id(id).get_attribute("value"))
                break
        
        if mode == False:
            if( str(val) != driver.find_element_by_id(id).text ):
                break

        if mode == 3 :
            # Temp Now Row
            PassTable = driver.find_element_by_css_selector(id)
            if(PassTable != val):
                break

def SaveTable (DataTable):

   # Open File And set mode Write
    with open('mrudTables.csv', 'w',encoding='utf-8', newline='') as csvfile:
        
        # Head
        fieldnames = ['DetaleID', 'MapingID', 'Area', 'District', 'DateOfContract', 'Space', 'Age(years)', 'TotalPriceOfToman']
        
        # Config head
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write Head
        writer.writeheader()
        
        for row in DataTable:
            # Write Row
            writer.writerow({fieldnames[0]: row[0], fieldnames[1]: row[1], fieldnames[2]: row[2], fieldnames[3]: row[3], fieldnames[4]: row[4], fieldnames[5]: row[5], fieldnames[6]: row[6], fieldnames[7]: row[7]})

# value Init
Table = []
Logs = []
StartYear = "1391" # set Value Year --> 1391 - 1398
StartMonth = "01" # set Value Mont --> 01 Farvardin
RowTemp = []
Page = 2
MaxLen = 11
url = 'http://hmi.mrud.ir'

# config drive
driver = webdriver.Chrome("C:/webdrivers/chromedriver.exe")

# GoTo url
driver.get(url)

# Wating Load
assert "سامانه اطلاعات بازار املاک ایران" in driver.title

# Select login
loginBTN = driver.find_element_by_name("btnsearch").click()

"""********************
    Start Scipts
********************"""
# Value Script
scripts = [
    '$("#ctl00_ContentPlaceHolder1_ASPxSplitter1_txtSDate_cboYear").val("{}")'.format(StartYear), # set Value Year --> 1391 - 1398
    '$("#ctl00_ContentPlaceHolder1_ASPxSplitter1_txtSDate_cboMonth").val("01")'.format(StartMonth), # set Value Mont --> 01 Farvardin
    '$("#ctl00_ContentPlaceHolder1_ASPxSplitter1_butSearch").click()', # Click button filter Table
    'document.getElementById("ctl00_ContentPlaceHolder1_ASPxSplitter1_CallbackPaneldgd_dgdlist_PagerBarB_butGoto_I").value = ', # Set VAlue Input PAge Number
    'document.getElementById("ctl00_ContentPlaceHolder1_ASPxSplitter1_CallbackPaneldgd_dgdlist_PagerBarB_butGoPageButton").click()', # Click Goto Page Number
    'document.getElementById("ctl00_ContentPlaceHolder1_ASPxSplitter1_CallbackPaneldgd_dgdlist_PagerBarB_butNextPageButton").click()' # Btn Next Page
]

"""********************
    Stop Scipts
********************"""

# Table Mode
driver.find_element_by_id('ctl00_ContentPlaceHolder1_ASPxSplitter1_CallbackPaneldgd_rdList_S_D').click()

# set Date
driver.execute_script(scripts[0])
driver.execute_script(scripts[1])
driver.execute_script(scripts[2])

# whating For Page Data Response
Whating('ctl00_ContentPlaceHolder1_ASPxSplitter1_CallbackPaneldgd_dgdlist','رکوردی موجود نیست',False)

time.sleep(2)

# print One index
print('-----------------------1-----------------------')

# Get Table
while Page <= MaxLen :
    try:
        # Get Rows
        TableTemp = driver.find_elements_by_css_selector('tr.dxgvDataRow_Aqua td')
        
        # Parse
        for row in TableTemp :
            # colemn
            col = row.text

            if col != '':
                # Insert Colemn
                RowTemp.append(col)

            else:
                try:
                    ID = row.find_elements_by_css_selector('script')[0].get_attribute("id")                
                    RowTemp.append(ID)

                except :
                    # Finally Row --> save
                    if len(RowTemp) == 8 :
                        Table.append(RowTemp)
                    else: # Program Log
                        Logs.append( 'Page = {} , No mach len colemn : {}'.format(Page,RowTemp) )

                    # Reset Catch File
                    RowTemp = []
       
        # Next Page
        driver.execute_script(scripts[3]+str(Page)+';')
        driver.execute_script(scripts[4])

        # Load Page Data
        if Page == 2 :
            time.sleep(25)
            driver.execute_script(scripts[3]+str(Page)+';')
            driver.execute_script(scripts[4])
        
        # Whating Page Next
        # Whating('tr.dxgvDataRow_Aqua td', TableTemp , 3)
        
        # Status
        print('-----------------------{}-----------------------'.format(Page))

        Page += 1
    except:
        print('Exeption')

SaveTable(Table)

driver.close()


