import csv, time, random, pandas as pd, schedule
from datetime import datetime, timedelta
from datetime import time as datetime_time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import os
import io
import json
from input import state_expansion
from apollo_main_driver import combine_csv_files

state_expansion.expand()

# Global variables to maintain state
last_processed_index = 0
last_processed_page = 1
last_processed_person = -1

run_code = False
start_time = ""
WEEKDAY = True
def read_json_values(json_file):
    global last_processed_index,last_processed_page,last_processed_person
    with open(json_file, 'r') as file:
        data = json.load(file)
        last_processed_index = data.get('last_processed_index', 0)
        last_processed_page = data.get('last_processed_page', 1)
        last_processed_person = data.get('last_processed_person', -1)
    return last_processed_index, last_processed_page, last_processed_person
read_json_values("settings_apollo_1.json")
def update_last_processed_index(json_file, new_value):
    global last_processed_index, last_processed_page, last_processed_person
    with open(json_file, 'r+') as file:
        data = json.load(file)
        data['last_processed_index'] = new_value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def update_last_processed_page(json_file, new_value):
    global last_processed_index, last_processed_page, last_processed_person
    with open(json_file, 'r+') as file:
        data = json.load(file)
        data['last_processed_page'] = new_value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def update_last_processed_person(json_file, new_value):
    global last_processed_index, last_processed_page, last_processed_person
    with open(json_file, 'r+') as file:
        data = json.load(file)
        data['last_processed_person'] = new_value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
def is_company_saved(csv_file, company_name):
    with open(csv_file, "rb") as file:
        # Wrap the binary file object with a TextIOWrapper and specify the encoding
        csvfile = io.TextIOWrapper(file, encoding='latin-1', errors='ignore')
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        for row in reader:
            if row and row[0] == company_name:  # Check if row exists before accessing its elements
                return True
    return False
# Function to export unique records to output file
def export_to_file(records, filename):
    # Placeholder code for exporting records to output file
    print(f"Exporting records to {filename}")


# Function to check if it's time to take off for about 3-7 min
def take_break():
    global start_time, run_code
    if run_code:
        current_time = datetime.now()
        time_difference = current_time - start_time
        print(f"current time : {datetime.now().strftime('%H:%M:%S')}")
        if time_difference >= timedelta(hours=1):
            break_after_hour = random.randint(180, 420)
            print(f"Taking a break for {break_after_hour} seconds...")
            time.sleep(break_after_hour)
            start_time = datetime.now()

def random_sleep():
    time.sleep(random.randint(4, 7))
# Function to read the input file and for each record in the input file perform a search
def main():
    global last_processed_index,last_processed_page, run_code,last_processed_person  # Access global state variables
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()

    # assign a common user agent
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument(f"user-agent={my_user_agent}")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")

    # Create a new instance of ChromeDriver with the desired options
    try:
        driver = uc.Chrome(options=chrome_options)
    except Exception as e:
        print("Error occurred while initializing WebDriver:", e)
        return
    driver.maximize_window()

    # Create an ActionChains object
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)


    # Make a request to your target website.
    try:
        driver.get("https://app.apollo.io/#/login")
    except Exception as e:
        print("Error occurred while opening the website:", e)
        driver.quit()
        return

    email = "barry@dnc.com"
    password = "Mazen!1234"

    time.sleep(6)
    try:
        email_path = driver.find_element(By.XPATH, "(//form//input)[1]")
        for i in email:
            email_path.send_keys(i)
            time.sleep(random.uniform(0.2, 0.8))
        password_path = driver.find_element(By.XPATH, "(//form//input)[2]")
        for i in password:
            password_path.send_keys(i)
            time.sleep(random.uniform(0.2, 0.8))
        login_button = driver.find_element(By.XPATH, "//form//button")
        login_button.click()
        time.sleep(random.randint(3, 7))

    except Exception as e:
        print("Error occurred while logging in:", e)
        driver.quit()
        return

    wait = WebDriverWait(driver, 10)
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[@class="zp-link zp_OotKe zp_Xfylg"]')
            )
        )
        search_button = driver.find_element(
            By.XPATH, '(//a[@class="zp-link zp_OotKe zp_Xfylg"])'
        )
        search_button.click()
    except Exception as e:
        print("Error occurred while waiting for search element:", e)
        driver.quit()
        return

    try:
        input_file = os.getcwd()+r"/bot_use_only/input_1.csv"
        df = pd.read_csv(input_file)
        df.fillna("", inplace=True)
        print(df, "\n")
    except Exception as e:
        print("Error occurred while reading csv file:", e)
        driver.quit()
        return

    read_json_values("settings_apollo_1.json")
    for x in range(last_processed_index, len(df)):

        if run_code:
            first_name = df["First Name"][x]
            last_name = df["Last Name"][x]
            title = df["Title"][x]
            country = df["Country"][x]
            company = df["Company"][x]
            industry = df["Industry"][x]
            name = first_name + last_name
            print(f"Performing search for record: {df.iloc[x].to_dict()}")
            driver.save_screenshot("screen.png")
            if name:
                try:
                    name_accordian = driver.find_element(
                        By.XPATH, '(//div[@class="zp-accordion zp__jgHx zp_BOvnT"])[1]'
                    )
                    action.move_to_element(name_accordian).click().perform()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input',
                            )
                        )
                    )
                    name_input = driver.find_element(
                        By.XPATH,
                        '//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input',
                    )
                    time.sleep(random.randint(3, 5))
                    for i in name:
                        time.sleep(0.5)
                        name_input.send_keys(i)
                    time.sleep(3)
                    name_input.send_keys(Keys.ENTER)
                    time.sleep(3)
                    driver.find_element(
                        By.XPATH,
                        '//div[@class="zp-accordion zp_BRLTI zp__jgHx zp_BOvnT"]//div[@class="zp_kyS5O"]',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by name:", e)

            time.sleep(random.randint(3, 7))
            if country:
                try:
                    country_accordian = driver.find_element(
                        By.XPATH, '//div[@class="zp-accordion zp__jgHx zp_BOvnT"]//span[contains(text(),"Location")]'
                    )
                    action.move_to_element(country_accordian).click().perform()
                    time.sleep(2)
                    country_input = driver.find_element(
                        By.XPATH,
                        '(//div[@class="zp-select-main"]//input)[1]',
                    )
                    action.scroll_to_element(country_input).perform()
                    action.move_to_element(country_input).click().perform()
                    time.sleep(random.randint(3, 5))
                    # try:
                    #     ind = driver.find_element(
                    #         By.XPATH, '//div[@class="zp-select-indicators"]'
                    #     )
                    #     action.move_to_element(ind).click().perform()
                    # except:
                    #     print("unable to click")

                    for i in country:
                        time.sleep(0.5)
                        country_input.send_keys(i)
                        # country_input.send_keys(Keys.ENTER)
                    time.sleep(3)
                    country_input.click()
                    time.sleep(2)
                    country_input.send_keys(Keys.ENTER)
                    time.sleep(2)

                    # action.move_to_element(country_input).send_keys(Keys.ENTER).perform()
                    time.sleep(7)
                    driver.find_element(
                        By.XPATH,
                        '//div[@class="zp-accordion zp_BRLTI zp__jgHx zp_BOvnT"]//div[@class="zp_kyS5O"]',
                    ).click()
                except Exception as e:
                    driver.save_screenshot("screen.png")
                    print("Error occurred while searching by country:", e)

            time.sleep(random.randint(3, 7))

            if title:
                try:
                    title_accordian = driver.find_element(
                        By.XPATH, '//div[@class="zp-accordion zp__jgHx zp_BOvnT"]//span[contains(text(),"Job Titles")]'
                    )
                    action.move_to_element(title_accordian).click().perform()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '(//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input)[2]',
                            )
                        )
                    )
                    title_input = driver.find_element(
                        By.XPATH,
                        '(//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input)[2]',
                    )
                    time.sleep(random.randint(3, 5))
                    for i in title:
                        time.sleep(0.5)
                        title_input.send_keys(i)
                    time.sleep(3)
                    title_input.send_keys(Keys.ENTER)
                    time.sleep(3)
                    driver.find_element(
                        By.XPATH,
                        '//div[@class="zp-accordion zp_BRLTI zp__jgHx zp_BOvnT"]//div[@class="zp_kyS5O"]',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by title:", e)

            time.sleep(random.randint(3, 7))

            if company:
                try:
                    company_accordian = driver.find_element(
                        By.XPATH, '//div[@class="zp-accordion zp__jgHx zp_BOvnT"]//span[contains(text(),"Company")]'
                    ).click()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '(//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input)[2]',
                            )
                        )
                    )
                    company_input = driver.find_element(
                        By.XPATH,
                        '(//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input)[2]',
                    )
                    time.sleep(random.randint(3, 5))
                    for i in company:
                        time.sleep(0.5)
                        company_input.send_keys(i)
                    time.sleep(3)
                    company_input.send_keys(Keys.ENTER)
                    time.sleep(3)
                    driver.find_element(
                        By.XPATH,
                        '//div[@class="zp-accordion zp_BRLTI zp__jgHx zp_BOvnT"]//div[@class="zp_kyS5O"]',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by company:", e)

            if industry:
                try:
                    industry_accordian = driver.find_element(
                        By.XPATH, '//div[@class="zp-accordion zp__jgHx zp_BOvnT"]//span[contains(text(),"Industry")]'
                    ).click()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '(//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input)[2]',
                            )
                        )
                    )
                    industry_input = driver.find_element(
                        By.XPATH,
                        '(//div[@class="zp-accordion-body zp_IKT8q zp_ttV5C"]//input)[2]',
                    )
                    time.sleep(random.randint(3, 5))
                    for i in industry:
                        time.sleep(0.5)
                        industry_input.send_keys(i)
                    time.sleep(3)
                    industry_input.send_keys(Keys.ENTER)
                    time.sleep(3)
                    driver.find_element(
                        By.XPATH,
                        '//div[@class="zp-accordion zp_BRLTI zp__jgHx zp_BOvnT"]//div[@class="zp_kyS5O"]',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by industry:", e)
            random_sleep()
            #scrape and make page number
            complete_url = driver.current_url
            base_url,filter_url = complete_url.split("page=1")
            last_processed_page = last_processed_page
            update_last_processed_page("settings_apollo_1.json",last_processed_page)
            for page in range(last_processed_page,99):

                complete_url = base_url+f"page={last_processed_page}"+filter_url
                print(f"Filtered url is {complete_url}")
                try:
                    driver.get(complete_url)
                except:
                    return main()
                time.sleep(1)

                try:
                    #scrape all links from table
                    all_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="zp_xVJ20"]//a')))
                except Exception as e:
                    all_links = []
                for l in range(0,len(all_links)):
                    all_links[l] = all_links[l].get_attribute("href")
                print(len(all_links))
                if len(all_links)==0:
                    last_processed_page = 1
                    last_processed_person = -1
                    update_last_processed_page("settings_apollo_1.json", last_processed_page)
                    update_last_processed_person("settings_apollo_1.json", last_processed_person)
                    break
                for count,lead in enumerate(all_links,last_processed_person+1):
                    print(count)
                    company_info = {
                        "Company": "",
                        "# Employees": "",
                        "Annual Revenue": "",
                        "Company Address": "",
                        "Company City": "",
                        "Company Country": "",
                        "Company Linkedin Url": "",
                        "Company Name for Emails": "",
                        "Company Phone": "",
                        "Company Postal Code": "",
                        "Company State": "",
                        "Company Street": "",
                        "Facebook Url": "",
                        "Founded Year": "",
                        "Industry": "",
                        "Keywords": "",
                        "Last Raised At": "",
                        "Latest Funding": "",
                        "Latest Funding Amount": "",
                        "Logo Url": "",
                        "Number of Retail Locations": "",
                        "Primary Intent Score": "",
                        "Primary Intent Topic": "",
                        "Secondary Intent Score": "",
                        "Secondary Intent Topic": "",
                        "SEO Description": "",
                        "Short Description": "",
                        "SIC Codes": "",
                        "Technologies": "",
                        "Total Funding": "",
                        "Twitter Url": "",
                        "Website": "",
                        "Website_txt_use": ""
                    }
                    data = {
                        "First Name": "",
                        "Last Name": "",
                        "Title": "",
                        "Company": "",
                        "Company Name for Emails": "",
                        "Email": "",
                        "Email Status": "Valid",
                        "No of Employees": "",
                        "Seniority": "",
                        "Departments": "",
                        "Corporate Phone": "",
                        "Personal Phone": "",
                        "Industry": "",
                        "Keywords": "",
                        "Person Linkedin Url": "",
                        "Website": "",
                        "Company Linkedin Url": "",
                        "Facebook Url": "",
                        "Twitter Url": "",
                        "City": "",
                        "State": "",
                        "Country": "",
                        "Company Description": "",
                    }
                    last_processed_person = count
                    update_last_processed_person("settings_apollo_1.json",last_processed_person)
                    try:
                        driver.get(lead)
                    except:
                        return main()
                    time.sleep(random.randrange(2,4))
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="zp_Ln9Ws EditTarget"]//span')))
                    #person name
                    ename = driver.find_element(
                        By.XPATH, '//div[@class="zp_Ln9Ws EditTarget"]//span'
                    ).text
                    try:
                        efname, elname = str(ename).split(" ")
                    except:
                        efname = ename
                        elname = ""
                    data["First Name"] = efname
                    data["Last Name"] = elname

                    #personal linkedin
                    try:
                        linkedin_url = driver.find_element("xpath","(//a[@class='zp-link zp_OotKe'][contains(@href,'linkedin')])[1]").get_attribute("href")
                        data['Person Linkedin Url'] = linkedin_url
                    except:pass

                    #Title
                    try:
                        title = driver.find_element("xpath","//span[@class='zp_LkFHT']").text
                        data['Title'] = title
                        data['Seniority'] = title
                    except:pass

                    #Company name
                    try:
                        company = driver.find_element("xpath","//span[@class='zp_XlAqf']//a").text
                        data['Company'] = company
                        data['Company Name for Emails'] = company

                    except:pass

                    #Email
                    try:
                        try:
                            access_button = driver.find_element("xpath","//div[contains(text(),'Access Email & Phone Number')]//parent::button")
                            access_button.click()
                            # random_sleep()
                            time.sleep(random.randint(4, 6))
                        except:
                            pass
                        wait.until(EC.presence_of_element_located((By.XPATH,
                                                                   '//div[contains(text(),"Business")]/preceding-sibling::a[contains(text(),"@")]')))
                        email = driver.find_element("xpath","//div[contains(text(),'Business')]/preceding-sibling::a[contains(text(),'@')]").text
                        data['Email'] = email
                        try:
                            personal_email = driver.find_element("xpath","//div[contains(text(),'Personal')]/preceding-sibling::span[contains(text(),'@')]").text
                            data['Email']+="\n"+personal_email
                        except:
                            pass
                    except:pass

                    #personal phone number
                    try:
                        # personal_phone = driver.find_element("xpath","//a[contains(text(),'equest Mobi')]").click()

                        # time.sleep(random.randint(11, 16))
                        personal_phone = driver.find_element("xpath","//div[contains(text(),'Primary')]/preceding-sibling::div//span").text

                        try:
                            extra = driver.find_elements("xpath","//a[@class='zp-link zp_OotKe zp_lmMY6']//span")[-1].text
                            if extra != personal_phone:
                                personal_phone+="\n"+extra

                        except:pass
                        data['Personal Phone'] = personal_phone
                    except:pass

                    #person address
                    try:
                        p_address = driver.find_element("xpath","//div[text()='Location']/following-sibling::div").text
                        data['Country'] = country
                        data['City'] = p_address.split(", ")[0]
                        data['State'] = p_address.split(", ")[1]
                    except:pass

                    #scrape company details
                    try:
                        c_elemet = driver.find_element("xpath", "//span[@class='zp_XlAqf']//a")
                        action.move_to_element(c_elemet).click().perform()
                        print("company clicked")
                        random_sleep()
                        # random_sleep()
                        company_info['Company'] = company
                        company_info['Company Name for Emails'] = company

                    except:
                        pass

                    try:
                        company_phone_number = wait.until(EC.presence_of_element_located((By.XPATH, '//button//span[contains(text(),"(")]'))).text
                        data['Corporate Phone'] = company_phone_number
                        company_info['Company Phone'] = company_phone_number
                    except:pass

                    #Employees
                    try:
                        employees = driver.find_element("xpath","//span[contains(text(),'Leads')]//parent::a/parent::div/preceding-sibling::span").text
                        company_info['# Employees'] = employees
                        data['No of Employees'] = employees
                    except:
                        pass

                    #Annual revenue

                    try:
                        annual_revenue = driver.find_element("xpath","//div[contains(text(),'Annual Revenue')]/following-sibling::div").text
                        company_info['Annual Revenue'] = annual_revenue
                    except:pass

                    #company linkedin
                    try:
                        company_linkedin_url = driver.find_element("xpath","//a[contains(@href,'linkedin') and contains(@href,'company')]").get_attribute("href")
                        company_info['Company Linkedin Url'] = company_linkedin_url
                    except:pass

                    # company facebook
                    try:
                        company_facebook_url = driver.find_element("xpath",
                                                                   "//a[contains(@href,'facebook')]").get_attribute("href")
                        company_info['Facebook Url'] = company_facebook_url
                        data['Facebook Url'] = company_facebook_url
                    except:
                        pass

                    # company twitter
                    try:
                        company_twitter_url = driver.find_element("xpath",
                                                                       "//a[contains(@href,'twitter')]").get_attribute("href")
                        company_info['Twitter Url'] = company_twitter_url
                        data['Twitter Url'] = company_twitter_url
                    except:
                        pass

                    # company founded
                    try:
                        company_founded = driver.find_element("xpath",
                                                                       "//div[contains(text(),'Founding Year')]/following-sibling::div").text
                        company_info['Founded Year'] = company_founded
                    except:
                        pass

                    # company industry
                    try:
                        company_industry = driver.find_element("xpath",
                                                                  "//div[contains(text(),'Industry')]/following-sibling::div").text
                        company_info['Industry'] = company_industry
                        data['Industry'] = company_industry
                    except:
                        pass

                    #company keywords
                    try:
                        keywords = driver.find_element("xpath","//div[contains(text(),'Company Keywords')]/following-sibling::div").text
                        company_info['Keywords'] = keywords
                        data['Keywords'] = keywords
                    except:pass

                    #funding
                    try:
                        driver.find_element("xpath","//div[contains(text(),'Funding Rounds')]//parent::div/parent::a[@data-testid]").click()
                        time.sleep(4)
                        funding = driver.find_element("xpath","//div[@class='zp_Nu4rb']/div//span").text
                        print([funding],"==funding")
                        latest_funding  = funding
                        funding = funding.split("\n")
                        amount = funding[0]
                        date  = funding[-1]
                        company_info['Last Raised At'] = date
                        company_info['Latest Funding'] = latest_funding
                        company_info['Latest Funding Amount'] = amount
                    except:pass

                    #Logo url
                    try:
                        logo = driver.find_element("xpath","//img[contains(@src,'production')]").get_attribute("src")
                        company_info['Logo Url'] = logo
                    except:pass

                    #description
                    try:
                        short = driver.find_element("xpath","//div[@class='zp_r2pH_']").text
                        driver.find_element("xpath","//div[@class='zp_r2pH_']//a").click()
                        time.sleep(2)
                        long = driver.find_element("xpath","//div[@class='zp_r2pH_']").text
                        company_info['SEO Description'] = long
                        company_info['Short Description'] = short
                        data['Company Description'] = long
                    except:pass

                    #technologies

                    try:
                        driver.find_element("xpath",
                                            "//div[contains(text(),'Technologies')]//parent::div/parent::a").click()
                        time.sleep(3)
                        techs = driver.find_elements("xpath","//div[@class='zp_Nu4rb']//div[@class='zp_NbRbN']")
                        technologies = ""
                        for tech in techs:
                            technologies+=tech.text+","
                        print(technologies)
                        company_info['Technologies'] = technologies
                        data['Departments'] = technologies
                    except:pass

                    #company_website
                    try:
                        c_web = driver.find_element("xpath","//div[@class='zp_hpMiB']//a[@class='zp-link zp_OotKe']").get_attribute("href")
                        company_info['Website'] = c_web
                        company_info['Website_txt_use'] = c_web
                        data['Website'] = c_web
                    except:pass

                    #locations
                    try:
                        driver.find_element("xpath","//a[text()='Locations']").click()
                        time.sleep(4)
                        stores = driver.find_elements("xpath","//div[@data-cy]//small")
                        company_info['Number of Retail Location'] = len(stores)
                        if len(stores)>0:
                            address = stores[0].text
                            company_info['Company Address'] = address
                            company_info['Company City'] = address.split(", ")[1]
                            company_info['Company Country'] = address.split(", ")[3]
                            company_info['Company Postal Code'] = address.split(", ")[2]
                            company_info['Company State'] = address.split(", ")[2].split(" ")[0]
                            company_info['Company Street'] = address.split(", ")[0]
                    except:pass

                    csv_file_path = f"{os.getcwd()}/bot_use_only/output_apollo_1.csv"

                    # Check if the file exists and is empty
                    if os.path.exists(csv_file_path) == False:
                        # File is empty, write the header
                        with open(csv_file_path, "w", newline="") as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                            writer.writeheader()

                    # Write the dictionary to the CSV file in append mode
                    with open(csv_file_path, "a", newline="",encoding="utf-8") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                        writer.writerow(data)

                    csv_file_path = f"{os.getcwd()}/bot_use_only/output_apollo_company_1.csv"

                    # Check if the file exists and is empty
                    if os.path.exists(csv_file_path)==False:
                        # File is empty, write the header
                        with open(csv_file_path, "w", newline="",encoding="utf-8") as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=company_info.keys())
                            writer.writeheader()

                    company_name = company_info["Company"]

                    # Check if the company is already saved in the CSV file
                    if not is_company_saved(csv_file_path, company_name):
                        # Write the dictionary to the CSV file in append mode
                        with open(csv_file_path, "a", newline="",encoding="utf-8") as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=company_info.keys())

                            writer.writerow(company_info)
                    else:
                        print(f"Company '{company_name}' already exists in the CSV file.")

                    print(f"Data has been appended to {csv_file_path}")

                    file_paths = [f"{os.getcwd()}/bot_use_only/output_apollo_company_1.csv",
                                  f"{os.getcwd()}/bot_use_only/output_apollo_company_2.csv",
                                  f"{os.getcwd()}/bot_use_only/output_apollo_company_3.csv"]
                    output_file = 'output/output_apollo_company.csv'
                    combine_csv_files(file_paths, output_file)

                    file_paths = [f"{os.getcwd()}/bot_use_only/output_apollo_1.csv",
                                  f"{os.getcwd()}/bot_use_only/output_apollo_2.csv",
                                  f"{os.getcwd()}/bot_use_only/output_apollo_3.csv"]
                    output_file = 'output/output_apollo.csv'
                    combine_csv_files(file_paths, output_file)

                    # Take 3-12 seconds between searches mimic a lazy human
                    time.sleep(random.randint(2, 4))

                    if stop_code():
                        print("shift end!")
                        print(f"last_processed_index: {last_processed_index}")
                        break

                    take_break()

                last_processed_page = page+1
                update_last_processed_page("settings_apollo_1.json", last_processed_page)

                last_processed_person = -1
                update_last_processed_person("settings_apollo_1.json", last_processed_person)
                if stop_code():
                    print("shift end!")
                    print(f"last_processed_index: {last_processed_index}")
                    break

                take_break()
            last_processed_index = x + 1  # Update the last processed index
            last_processed_page = 1
            last_processed_person = -1
            update_last_processed_index("settings_apollo_1.json",last_processed_index)
            update_last_processed_page("settings_apollo_1.json",last_processed_page)
            update_last_processed_person("settings_apollo_1.json",last_processed_person)




            try:
                driver.get(
                    "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c"
                )
            except Exception as e:
                print("Error occurred while navigating to search page:", e)
                driver.quit()
                return

            if stop_code():
                print("shift end!")
                print(f"last_processed_index: {last_processed_index}")
                break

            take_break()

    if last_processed_index == len(df):
        print("search completed!")
        update_last_processed_index("settings_apollo_1.json",0)
        update_last_processed_person("settings_apollo_1.json",-1)
        update_last_processed_page("settings_apollo_1.json", 1)
        # export_to_file(df, "output/output_apollo.csv")
        print(f"current time : {datetime.now().strftime('%H:%M:%S')}")

    driver.quit()


def start_code():
    global run_code, start_time

    # random delay between 10-45 min to start
    # start_delay = random.randint(600, 2700)
    start_delay = random.randint(10, 15)
    print(f"Delay will be of {start_delay//60}:{start_delay%60} minutes.")
    time.sleep(start_delay)
    print(f"current time : {datetime.now().strftime('%H:%M:%S')}")

    run_code = True
    start_time = datetime.now()

    main()


# Function to check if it's time to stop the code
def stop_code():
    global run_code,WEEKDAY
    current_time = datetime.now()
    WEEKDAY = is_weekday()
    if WEEKDAY == True:
        if current_time.hour >= 20 and current_time.minute >= 30:
            run_code = False
            return True
    else:
        if current_time.hour >= 20 and current_time.minute >= 30:
            run_code = False
            return True

    return False


# Function to check if today is a weekday
def is_weekday():
    global WEEKDAY
    today = datetime.today().weekday()
    # Monday is 0 and Sunday is 6
    if 0 <= today <= 4:

        WEEKDAY = True
        return True
    else:

        WEEKDAY = False
        return False


if __name__ == "__main__":
    print("Program started...")

    while True:
        current_time = datetime.now().time()
        if is_weekday() == True:
            if datetime_time(1, 2) <= current_time < datetime_time(10, 2):
                if stop_code() == True:
                    continue
                print("Starting Code..")
                start_code()
        else:
            if datetime_time(1, 2) <= current_time < datetime_time(8, 2):
                if stop_code() == True:
                    continue
                print("Starting code...")
                start_code()
        time.sleep(1)
