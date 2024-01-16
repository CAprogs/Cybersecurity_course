import requests
import json
from bs4 import BeautifulSoup


def ask(message: str):
    """Ask the user for a response and return it.
    """

    try:
        response = input(message)
        return response
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        exit()


def get_json_info(json_data, id):
    """Get the information from a JSON file
    """    
    
    try:
        data = json_data.get(id)
        if data is None:
            data = "N/A"
        return data
    except Exception as e:
        print("Error : ", e)


# Exercice 1
def exo_1():
    """Ask the user for a URL and save the response in a file.
    """

    while True:
        try:
            url = ask("Enter a target URL (Ctrl + C to exit): ")
            response = requests.get(url)
            if response.status_code == 200:
                file_name = url.replace("https://", "").replace("http://", "").replace("www.", "").split(".")[0]

                datas = {
                    "url": url.replace(" ", ""), 
                    "html_content": response.text}

                with open(f"{file_name}.json", "w") as json_file:
                    json.dump(datas, json_file, indent=1)
                print("Information gathered from : ", url)
            else:
                print(f"\nCan't access this page ! Status code : {response.status_code}\n")
        except Exception as e:
            print("Error : ", e)


# Exercice 2
class Requests_performer:

    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code
        self.headers = self.response.headers
        self.content = self.response.content
        self.text = self.response.text

    def print_infos(self):
        print(f"""HTTP Headers Information:
Content-Type: {self.headers.get('Content-Type', 'N/A')}
Server: {self.headers.get('Server', 'N/A')}
Date: {self.headers.get('Date', 'N/ A')}
""")


def exo_2():
    """Ask the user for a URL and print the HTTP headers information.
    """

    while True:
        try:
            url = ask("Enter a target URL (Ctrl + C to exit): ")
            response = Requests_performer(url)
            if response.status_code == 200:
                response.print_infos()
            else:
                print(f"\nCan't access this page ! Status code : {response.status_code}\n")
        except Exception as e:
            print("Error : ", e)


# Exercice 3
def exo_3():
    """Perform a simple IP geolocation lookup using ipinfo.io's API.
    """

    while True:
        try:
            ip = ask("Enter an IP address (Ctrl + C to exit): ")
            response = requests.get("https://ipinfo.io/" + f"{ip}")
            if response.status_code == 200:
                infos_json = json.loads(response.text)
                print(f"""IP Geolocation Information:
IP Address: {get_json_info(infos_json, "ip")}
City: {get_json_info(infos_json, "city")}
Region: {get_json_info(infos_json, "region")}
Country: {get_json_info(infos_json, "country")}
Location: {get_json_info(infos_json, "loc")}
Organization: {get_json_info(infos_json, "org")}
Timezone: {get_json_info(infos_json, "timezone")}
AS (Autonomous System): {get_json_info(infos_json, "as")}""")
            else:
                print(f"\nCan't access this page ! Status code : {response.status_code}\n")
        except Exception as e:
            print("Error : ", e)


# Exercice 4
def exo_4():
    """Analyze a webpage, extract specific content, and perform basic data manipulation..
    """

    while True:
        try:
            url = ask("Enter a target URL (Ctrl + C to exit): ")
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                print(f"""Url: {url} \nTotal Number of Headings: {len(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]))}""")
                paragraphs = [p.text for p in soup.find_all("p")[:3]]
                print("First 3 paragraphs:")
                for index, paragraph in enumerate(paragraphs, start=1):
                    print(f"{index}. {paragraph}")
            else:
                print(f"\nCan't access this page ! Status code : {response.status_code}\n")
        except Exception as e:
            print("Error : ", e)


# Exercice 5
# webpage 1 : https://www.amazon.fr/deal/8315df54?showVariations=true
# webpage 2 : https://urlz.fr/pe9u
def exo_5():
    """Download a pdf or images from a webpage.
    """

    i = 0
    while True:
        try:
            url = ask("\nEnter a target URL (Ctrl + C to exit): ")
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            if response.status_code == 200:
                imgs = soup.find_all("img")
                if ".pdf" in url:
                    file_name = f"downloaded_document_{i}.pdf"
                    with open(file_name, "wb") as f:
                        f.write(response.content[0])
                    print(f"File '{file_name}' downloaded successfully. ")
                    i += 1
                elif imgs:
                    print(f"There is {len(imgs)} images in this page.")
                    response = ask("""\nDownload all images : (A)\nDownload a single image : (B)\nEnter another url : (C)\nExit : (Ctrl + C)\n\n      >>>>""")
                    
                    if response.lower() == "a":
                        for index, img in enumerate(imgs, start=0):
                            file_name = f"image_{index}.jpg"
                            try:
                                img_response = requests.get(img.attrs['src'])
                                with open(file_name, 'wb') as f:
                                    f.write(img_response.content)
                                print(f"File '{file_name}' downloaded successfully.")
                                i += 1
                            except Exception as e:
                                print("Error : ", e)
                                if index == len(imgs):
                                    print("Downloaded files")
                                else:
                                    continue
                    elif response.lower() == "b":
                        indexes = [index for index, img in enumerate(imgs, start=0)]
                        index = ask(f"\nEnter the index of the image you want to download.\n Indexes : {indexes}\n\n      >>>>")
                        if index.isdigit() and int(index) in indexes:
                            file_name = f"image_{index}.jpg"
                            img_response = requests.get(imgs[int(index)].attrs['src'])
                            with open(file_name, 'wb') as f:
                                f.write(img_response.content)
                            print(f"File '{file_name}' downloaded successfully.")
                            i += 1
                        else:
                            print("\nThis index doesn't exist. Try again.")
                    elif response.lower() == "c":
                        pass
                    else:
                        print("\nInvalid response. Try again.")
                else:
                    print("There is nothing to download in this page.")
            else:
                print(f"\nCan't access this page ! Status code : {response.status_code}\n")
        except Exception as e:
            print("Error : ", e)


if __name__ == '__main__':
    exo_1()
    #exo_2()
    #exo_3()
    #exo_4()
    #exo_5()
