import csv, time, random, pandas as pd
import undetected_chromedriver as uc
from datetime import datetime, timedelta
from datetime import time as datetime_time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
import io
import json
from input import state_expansion

# state_expansion.expand()

# Global variables to maintain state
last_processed_index = 0
last_processed_page = 5
last_processed_person = 1
last_page_url = None
run_code = False
start_time = ""
WEEKDAY=True

def read_json_values(json_file):
    global last_processed_index,last_processed_page,last_processed_person,last_page_url
    with open(json_file, 'r') as file:
        data = json.load(file)
        last_processed_index = data.get('last_processed_index', 0)
        last_processed_page = data.get('last_processed_page', 1)
        last_processed_person = data.get('last_processed_person', -1)
        last_page_url = data.get('last_page_url', None)
    return last_processed_index, last_processed_page, last_processed_person
read_json_values("settings_zoominfo.json")

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
        
def update_last_page_url(json_file, new_value):
    global last_processed_index, last_processed_page, last_processed_person,last_page_url
    with open(json_file, 'r+') as file:
        data = json.load(file)
        data['last_page_url'] = new_value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
def is_company_saved(csv_file, company_name):
    with open(csv_file, "rb") as file:
        # Wrap the binary file object with a TextIOWrapper and specify the encoding
        csvfile = io.TextIOWrapper(file, encoding="latin-1", errors="ignore")
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        for row in reader:
            if (
                row and row[0] == company_name
            ):  # Check if row exists before accessing its elements
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
    time.sleep(random.randint(3, 6))


# Function to read the input file and for each record in the input file perform a search
def main():
    global last_processed_index, last_processed_page, run_code, last_processed_person,last_page_url  # Access global state variables
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()


    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    # Set up Chrome options
    driver = uc.Chrome(user_data_dir=os.getcwd()+"/zoominfo",options=chrome_options)
    driver.maximize_window()

    # Make a request to your target website.
    try:
        driver.get("https://login.zoominfo.com/")
        time.sleep(10)

        # Get the current URL
        current_url = driver.current_url
        if "login.zoominfo.com" in current_url:
            username = "bkunst@dnc.com"
            password = "Mazen!13"

            input_username = driver.find_element(
                By.XPATH, '//input[@id="okta-signin-username"]'
            )
            input_username.clear()
            for i in username:
                input_username.send_keys(i)
                time.sleep(random.uniform(0.2, 0.8))
            input_password = driver.find_element(
                By.XPATH, '//input[@id="okta-signin-password"]'
            )
            input_password.clear()
            for i in password:
                input_password.send_keys(i)
                time.sleep(random.uniform(0.2, 0.8))

            login_button = driver.find_element(By.XPATH, '//input[@id="okta-signin-submit"]')
            login_button.click()
            time.sleep(8)
            try:
                otp_box = driver.find_element(By.XPATH, '//input[@id="verify-code-input"]')
                otp = input("Enter OTP:")

                for i in otp:
                    otp_box.send_keys(i)
                    time.sleep(random.uniform(0.2, 0.8))
                verify = driver.find_element(By.XPATH, '//button[@id="verify-btn"]')
                verify.click()
                time.sleep(5)
            except:
                pass
    except Exception as e:
        print("Error occurred while opening the website:", e)
        input("Please check...")

    # Create an ActionChains object
    action = ActionChains(driver)

    wait = WebDriverWait(driver, 20)
    # try:
    #     wait.until(
    #         EC.presence_of_element_located(
    #             (
    #                 By.XPATH,
    #                 '//div[@class="application-header ng-star-inserted"]//button',
    #             )
    #         )
    #     )
    #     search_button = driver.find_element(
    #         By.XPATH, '//div[@class="application-header ng-star-inserted"]//button'
    #     )
    #     search_button.click()
    # except Exception as e:
    #     print("Error occurred while waiting for search element:", e)
    #     driver.quit()
    #     return

    try:
        input_file = "input/expanded_input.csv"
        df = pd.read_csv(input_file)
        df.fillna("", inplace=True)
        # print(df, "\n")
    except Exception as e:
        print("Error occurred while reading csv file:", e)
        driver.quit()
        return
    input()
    for x in range(last_processed_index, len(df)):
        try:
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//div[@class="application-header ng-star-inserted"]//button',
                    )
                )
            )
            search_button = driver.find_element(
                By.XPATH, '//div[@class="application-header ng-star-inserted"]//button'
            )
            search_button.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-clear-all']"))
            ).click()

        except Exception as e:
            pass
        if run_code:
            first_name = df["First Name"][x]
            last_name = df["Last Name"][x]
            title = df["Title"][x]
            country = df["Country"][x].split(", ")[0].strip()
            company = df["Company"][x]
            industry = df["Industry"][x]
            name = first_name + last_name
            print(f"Performing search for record: {df.iloc[x].to_dict()}")
            # print(f"Getting page https://app.zoominfo.com/#/apps/searchV2/v2/saved ")
            # driver.get("https://app.zoominfo.com/#/apps/searchV2/v2/saved")

            time.sleep(10)
            if name:
                try:
                    name_accordian = driver.find_element(
                        By.XPATH, '//div[@id="contactName'
                    )
                    action.move_to_element(name_accordian).click().perform()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//input[contains(@id,"fullName_")]',
                            )
                        )
                    )
                    name_input = driver.find_element(
                        By.XPATH,
                        '//input[contains(@id,"fullName_")]',
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
                        '//div[@id="contactName"]//zic-button',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by name:", e)

            # time.sleep(random.randint(3, 12))
            random_sleep()
            if country:
                try:
                    country_accordian = driver.find_element(
                        By.XPATH, '//div[@id="locations"]'
                    )
                    action.move_to_element(country_accordian).click().perform()
                    time.sleep(1.5)
                    country_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@data-automation-id="locations-filter-country-state-city-input"]'))
                        )
                    action.scroll_to_element(country_input).perform()
                    action.move_to_element(country_input).click().perform()
                    time.sleep(2)
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
                    time.sleep(2)
                    country_input.click()
                    time.sleep(1)
                    country_input.send_keys(Keys.ENTER)
                    time.sleep(2)

                    # action.move_to_element(country_input).send_keys(Keys.ENTER).perform()
                    # time.sleep()
                    driver.find_element(
                        By.XPATH,
                        '//div[@id="locations"]//zic-button',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by country:", e)

            # time.sleep(random.randint(3, 12))
            random_sleep()
            if title:
                try:
                    print(title)
                    driver.save_screenshot("test.png")
                    title_accordian = driver.find_element(
                        By.XPATH, '//div[@id="currentRole"]'
                    )
                    action.move_to_element(title_accordian).click().perform()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//input[@data-automation-id="currentRole-filter-jobTitle-input"]',
                            )
                        )
                    )
                    title_input = driver.find_element(
                        By.XPATH,
                        '//input[@data-automation-id="currentRole-filter-jobTitle-input"]',
                    )
                    action.scroll_to_element(title_input).perform()
                    action.move_to_element(title_input).click().perform()
                    time.sleep(random.randint(3, 5))

                    for i in title:
                        time.sleep(0.5)
                        title_input.send_keys(i)
                    time.sleep(1)
                    title_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                    driver.find_element(
                        By.XPATH,
                        '//div[@id="currentRole"]//zic-button',
                    ).click()
                except:
                    pass
                    # print("Error occurred while searching by title:", e)

            # time.sleep(random.randint(3, 12))
            random_sleep()
            if company:
                try:
                    company_accordian = driver.find_element(
                        By.XPATH, '//div[@id="companyNameUrlTicker"]'
                    ).click()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//input[@data-automation-id="company-name-filter-input"]',
                            )
                        )
                    )
                    company_input = driver.find_element(
                        By.XPATH,
                        '//input[@data-automation-id="company-name-filter-input"]',
                    )
                    time.sleep(random.randint(3, 5))
                    for i in company:
                        time.sleep(0.5)
                        company_input.send_keys(i)
                    time.sleep(1)
                    company_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                    driver.find_element(
                        By.XPATH,
                        '//div[@id="companyNameUrlTicker"]//zic-button',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by company:", e)

            if industry:
                try:
                    industry_accordian = driver.find_element(
                        By.XPATH, '//div[@id="industry"]'
                    ).click()
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//input[@name="industry-keywords-input"]',
                            )
                        )
                    )
                    industry_input = driver.find_element(
                        By.XPATH,
                        '//input[@name="industry-keywords-input"]',
                    )
                    time.sleep(random.randint(3, 5))
                    for i in industry:
                        time.sleep(0.5)
                        industry_input.send_keys(i)
                    time.sleep(1)
                    industry_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                    driver.find_element(
                        By.XPATH,
                        '//div[@id="industry"]//zic-button',
                    ).click()
                except Exception as e:
                    print("Error occurred while searching by industry:", e)
            random_sleep()
            # scrape and make page number
            # input("--")
            # wait.until(
            #     EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr"))
            # )
            pages = driver.find_elements(
                By.XPATH, '//span[@class="p-paginator-pages ng-star-inserted"]//button'
            )
            #set page first
            if last_page_url!=None:
                driver.get(last_page_url)
                time.sleep(5)
            last_processed_page = last_processed_page
            update_last_processed_page("settings_zoominfo.json", last_processed_page)
            for page in range(last_processed_page,100):
                listofNames = driver.find_elements(By.XPATH, "//table//tbody//tr")
                print(len(listofNames))
                all_links = driver.find_elements("xpath","//a[@data-automation-id='contact-column-contact-name']")
                for l in range(0, len(all_links)):
                    all_links[l] = all_links[l].get_attribute("href")
                if len(all_links)==0:
                    last_processed_page = 1
                    last_processed_person = -1
                    last_page_url = None
                    update_last_processed_page("settings_zoominfo.json", last_processed_page)
                    update_last_processed_person("settings_zoominfo.json", last_processed_person)
                    update_last_page_url("settings_zoominfo.json",last_page_url)
                    break
                last_page_url = driver.current_url
                update_last_page_url("settings_zoominfo.json",last_page_url)
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
                        "Website_txt_use": "",
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
                    update_last_processed_person("settings_zoominfo.json", last_processed_person)
                    try:
                        driver.get(lead)
                    except:
                        pass
                    random_sleep()
                    try:
                        # wait.until(
                        #     EC.element_to_be_clickable(
                        #         (
                        #             By.XPATH,
                        #             '//a[@data-automation-id="contact-column-contact-name"]',
                        #         )
                        #     )
                        # )
                        # name_link = driver.find_element(
                        #     By.XPATH,
                        #     f'(//a[@data-automation-id="contact-column-contact-name"])[{j+1}]',
                        # ).click()
                        # random_sleep()
                        # person name
                        ename = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-automation-id="person-name"]'))).text
                        try:
                            efname, elname = str(ename).split(" ")
                        except:
                            try:
                                efname, elname = str(ename).split(".")
                            except:
                                efname = ename
                                elname = ""
                        data["First Name"] = efname
                        data["Last Name"] = elname

                        # personal linkedin
                        # try:
                        #     linkedin_url = driver.find_element("xpath","(//a[@class='zp-link zp_OotKe'][contains(@href,'linkedin')])[1]").get_attribute("href")
                        #     data['Person Linkedin Url'] = linkedin_url
                        # except:pass

                        # Title
                        try:
                            title = driver.find_element(
                                "xpath",
                                '//div[@class="contact-details__title truncate-text"]',
                            ).text
                            data["Title"] = title
                            data["Seniority"] = title
                        except:
                            pass

                        # Company name
                        try:
                            company = driver.find_element(
                                "xpath", '//div[@class="company-details__link-row"]'
                            ).text
                            data["Company"] = company
                            data["Company Name for Emails"] = company
                            company_info["Company"] = company
                            company_info["Company Name for Emails"] = company

                        except:
                            pass

                        # Email
                        try:
                            email = driver.find_element(
                                "xpath", "//a//span[contains(text(),'@')]"
                            ).text
                            data["Email"] = email
                        except:
                            pass

                        # personal phone number
                        try:
                            # personal_phone = driver.find_element("xpath","//a[contains(text(),'equest Mobi')]").click()

                            # time.sleep(random.randint(11, 16))
                            personal_phone = driver.find_element(
                                "xpath", "//a[contains(@data-automation-id,'Mobile')]"
                            ).text

                            data["Personal Phone"] = personal_phone
                        except:
                            pass

                        # corporate phone number
                        try:
                            company_phone_number = driver.find_element(
                                "xpath", "//a[contains(@data-automation-id,'HQ')]"
                            ).text
                            data["Corporate Phone"] = company_phone_number
                            company_info["Company Phone"] = company_phone_number
                        except:
                            pass

                        # #scrape company details
                        # try:
                        #     c_elemet = driver.find_element("xpath", "//span[@class='zp_XlAqf']//a")
                        #     action.move_to_element(c_elemet).click().perform()
                        #     print("company clicked")
                        #     random_sleep()
                        #     random_sleep()
                        #     company_info['Company'] = company
                        #     company_info['Company Name for Emails'] = company

                        # except:
                        #     pass

                        # Employees
                        try:
                            employees = driver.find_element(
                                "xpath", "//div[contains(text(),'estimated employees')]"
                            ).text
                            company_info["# Employees"] = employees
                            data["No of Employees"] = employees
                        except:
                            pass

                        # Annual revenue

                        try:
                            annual_revenue = driver.find_element(
                                "xpath", "//div[contains(text(),'$')]"
                            ).text
                            company_info["Annual Revenue"] = annual_revenue
                        except:
                            pass

                        # #company linkedin
                        # try:
                        #     company_linkedin_url = driver.find_element("xpath","//a[contains(@href,'linkedin') and contains(@href,'company')]").get_attribute("href")
                        #     company_info['Company Linkedin Url'] = company_linkedin_url
                        # except:pass

                        # # company facebook
                        # try:
                        #     company_facebook_url = driver.find_element("xpath",
                        #                                                "//a[contains(@href,'facebook')]").get_attribute("href")
                        #     company_info['Facebook Url'] = company_facebook_url
                        #     data['Facebook Url'] = company_facebook_url
                        # except:
                        #     pass

                        # # company twitter
                        # try:
                        #     company_twitter_url = driver.find_element("xpath",
                        #                                                    "//a[contains(@href,'twitter')]").get_attribute("href")
                        #     company_info['Twitter Url'] = company_twitter_url
                        #     data['Twitter Url'] = company_twitter_url
                        # except:
                        #     pass

                        # company industry
                        try:
                            overview = driver.find_element(
                                "xpath", "//li[contains(@id,'Overview')]"
                            )
                            action.move_to_element(overview).click().perform()
                            time.sleep(2)
                            company_industry = driver.find_elements(
                                "xpath",
                                "//div[contains(@aria-label,'Industry')]//zi-attribute-chip",
                            )

                            # multiple elemets how to store in a list?
                            industries=""
                            for i in company_industry:
                                industries+=i.text+", "

                            company_info['Industry'] = industries
                            data['Industry'] = industries
                        except:
                            pass

                        # company founded
                        try:
                            company_founded = driver.find_element(
                                "xpath", "//span[contains(text(),'Year Founded')]"
                            ).text
                            string, company_founded = str(company_founded).split(": ")
                            company_info["Founded Year"] = company_founded
                        except:
                            pass

                        # company keywords
                        try:
                            k_e = driver.find_element("xpath","//li[@data-automation-id]//span[contains(text(),'Products & Services')]/parent::div/parent::div/parent::li")
                            action.move_to_element(k_e).click().perform()
                            time.sleep(2)
                            keywords_elems = driver.find_elements("xpath","//div[contains(@aria-label,'Products & Services')]//zi-attribute-chip")
                            keywords=""
                            for kwd in keywords_elems:
                                keywords+=kwd.text+", "
                            print("keywords= ",keywords)
                            company_info['Keywords'] = keywords
                            data['Keywords'] = keywords
                        except:pass

                        # funding
                        # try:
                        #     driver.find_element("xpath","//div[contains(text(),'Funding Rounds')]//parent::div/parent::a[@data-testid]").click()
                        #     random_sleep()
                        #     funding = driver.find_element("xpath","//div[@class='zp_Nu4rb']/div//span").text
                        #     print([funding],"==funding")
                        #     latest_funding  = funding
                        #     funding = funding.split("\n")
                        #     amount = funding[0]
                        #     date  = funding[-1]
                        #     company_info['Last Raised At'] = date
                        #     company_info['Latest Funding'] = latest_funding
                        #     company_info['Latest Funding Amount'] = amount
                        # except:pass

                        # Logo url
                        try:
                            logo = driver.find_element(
                                "xpath",
                                "//div[contains(@data-automation-id,'row-company-logo')]//img",
                            ).get_attribute("src")
                            company_info["Logo Url"] = logo
                        except:
                            pass

                        # description
                        try:
                            short = driver.find_element(
                                "xpath",
                                "//zi-text[contains(@data-automation-id,'profile-content-description')]//span",
                            ).text
                            driver.find_element(
                                "xpath", '//div[@aria-label="Show more description"]//span'
                            ).click()
                            time.sleep(1)
                            long = driver.find_element(
                                "xpath",
                                "//zi-text[contains(@data-automation-id,'profile-content-description')]//span",
                            ).text
                            company_info["SEO Description"] = long
                            company_info["Short Description"] = short
                            data["Company Description"] = long
                        except:
                            pass

                        # technologies

                        try:
                            driver.find_element(
                                "xpath",
                                "//span[contains(text(),'Technologies')]/parent::div/parent::div/parent::li",
                            ).click()
                            time.sleep(1.4)
                            techs = driver.find_elements(
                                "xpath", "//li[@role='option']"
                            )
                            technologies = ""
                            for tech in techs:
                                technologies += tech.text + ","
                            print(technologies)
                            company_info["Technologies"] = technologies
                            data["Departments"] = technologies
                        except:
                            pass

                        # company_website
                        try:
                            c_web = driver.find_element(
                                "xpath", '//a[@class="ng-binding url truncate-text"]'
                            ).get_attribute("href")
                            company_info["Website"] = c_web
                            company_info["Website_txt_use"] = c_web
                            data["Website"] = c_web
                        except:
                            pass

                        csv_file_path = f"{os.getcwd()}/output/output_zoominfo.csv"

                        # Check if the file exists and is empty
                        if os.path.exists(csv_file_path) == False:
                            # File is empty, write the header
                            with open(csv_file_path, "w", newline="") as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                                writer.writeheader()

                        # Write the dictionary to the CSV file in append mode
                        with open(
                            csv_file_path, "a", newline="", encoding="utf-8"
                        ) as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                            writer.writerow(data)

                        csv_file_path = f"{os.getcwd()}/output/output_zoominfo_company.csv"

                        # Check if the file exists and is empty
                        if os.path.exists(csv_file_path) == False:
                            # File is empty, write the header
                            with open(
                                csv_file_path, "w", newline="", encoding="utf-8"
                            ) as csvfile:
                                writer = csv.DictWriter(
                                    csvfile, fieldnames=company_info.keys()
                                )
                                writer.writeheader()

                        company_name = company_info["Company"]

                        # Check if the company is already saved in the CSV file
                        if not is_company_saved(csv_file_path, company_name):
                            # Write the dictionary to the CSV file in append mode
                            with open(
                                csv_file_path, "a", newline="", encoding="utf-8"
                            ) as csvfile:
                                writer = csv.DictWriter(
                                    csvfile, fieldnames=company_info.keys()
                                )

                                writer.writerow(company_info)
                        else:
                            print(
                                f"Company '{company_name}' already exists in the CSV file."
                            )

                        print(f"Data has been appended to {csv_file_path}")
                        # Take 3-12 seconds between searches mimic a lazy human
                        # time.sleep(random.randint(3, 12))
                    except Exception as e:
                        pass
                        print(e)
                        

                    # driver.get(current_url)
                    time.sleep(3)
                    if stop_code():
                        print("shift end!")
                        print(f"last_processed_index: {last_processed_index}")
                        break

                    take_break()
                try:
                    driver.get(last_page_url)
                    time.sleep(5)
                    driver.find_element(By.XPATH, '//button[@class="p-ripple p-element p-paginator-next p-paginator-element p-link"]').click()
                    random_sleep()
                    last_page_url = driver.current_url
                    update_last_page_url("settings_zoominfo.json",last_page_url)
                    last_processed_page = page + 1
                    update_last_processed_page("settings_zoominfo.json", last_processed_page)

                except:
                    last_page_url = None
                    update_last_page_url("settings_zoominfo.json", last_page_url)
                    last_processed_page = 1
                    update_last_processed_page("settings_zoominfo.json", last_processed_page)

                    last_processed_person = -1
                    update_last_processed_person("settings_zoominfo.json", last_processed_person)
                    print("break as next page not found")
                    break
                # last_processed_page = page + 1
                # update_last_processed_page("settings_zoominfo.json", last_processed_page)

                last_processed_person = -1
                update_last_processed_person("settings_zoominfo.json", last_processed_person)

                last_processed_index = x + 1
                update_last_processed_index("settings_zoominfo.json", last_processed_index)

                if stop_code():
                    print("shift end!")
                    print(f"last_processed_index: {last_processed_index}")
                    break

                take_break()

            if stop_code():
                print("shift end!")
                print(f"last_processed_index: {last_processed_index}")
                break

            take_break()

            try:
                driver.get("https://app.zoominfo.com/#/apps/home-page")

            except Exception as e:
                print("Error occurred while navigating to search page:", e)
                driver.quit()
                return

    last_processed_index = x + 1  # Update the last processed index
    last_processed_page = 1
    last_processed_person = -1
    last_page_url = None
    update_last_processed_index("settings_zoominfo.json", last_processed_index)
    update_last_processed_page("settings_zoominfo.json", last_processed_page)
    update_last_processed_person("settings_zoominfo.json", last_processed_person)
    update_last_page_url("settings_zoominfo.json",last_page_url)

    if last_processed_index == len(df):
        print("search completed!")
        update_last_processed_index("settings_zoominfo.json", 0)
        update_last_processed_person("settings_zoominfo.json", -1)
        update_last_processed_page("settings_zoominfo.json", 1)
        update_last_page_url("settings_zoominfo.json", None)
        # export_to_file(df, os.getcwd()+"/output/output_zoominfo.csv")
        print(f"current time : {datetime.now().strftime('%H:%M:%S')}")

    driver.quit()


def start_code():
    global run_code, start_time

    # random delay between 10-45 min to start
    # start_delay = random.randint(600, 2700)
    # start_delay = random.randint(10, 15)
    # print(f"Delay will be of {start_delay//60}:{start_delay%60} minutes.")
    # time.sleep(start_delay)
    print(f"current time : {datetime.now().strftime('%H:%M:%S')}")

    run_code = True
    start_time = datetime.now()

    main()


# Function to check if it's time to stop the code
def stop_code():
    global run_code,WEEKDAY
    # return False
    current_time = datetime.now()
    WEEKDAY = is_weekday()
    if WEEKDAY == True:
        if current_time.hour >= 8 and current_time.minute >= 25:
            run_code = False
            return True
    else:
        if current_time.hour >= 8 and current_time.minute >= 25:
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
        # start_code()
        if is_weekday() == True:
            if datetime_time(20, 35) <= current_time:
                if stop_code()==True:
                    continue
                print("Starting Code..")
                start_code()
        else:
            if datetime_time(20, 35) <= current_time:
                if stop_code()==True:
                    continue
                print("Starting code...")
                start_code()
        time.sleep(1)
