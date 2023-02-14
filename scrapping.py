from typing import Optional, List, Dict
from tqdm import tqdm
import pandas as pd
import requests
from matplotlib import pyplot as plt
from sqlalchemy import create_engine


class GetData:
    """Get data from web scrapping."""

    def __init__(self, page: Optional[int] = 1) -> None:
        self.page = page
        self.response = None
        self.cookies = {}
        self.headers = {}
        self.data = {}
        self.err = None

    def __call__(self) -> Dict | str:
        """Get Cookies, Headers and Data that will be sent in a POST request"""
        self.cookies = {
            "visid_incap_2269415": "utV+Ruk/RAyxuFWIanYcf8mX5WMAAAAAQUIPAAAAAAC8lkjztHeeLfES/OFjWY1H",
            "nlbi_2269415": "U32xJnjMDQ6169Fm+0V6nQAAAABQVgXhZbvfNK2WJXhnd4hj",
            "incap_ses_675_2269415": "DApAUot8KxPIFWH+yxVeCcqX5WMAAAAANjGTJgA/zewzneUJZ6dGrg==",
            "gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko": "gigya-pr_ver4",
            "reese84": "3:x/ItUa/LEhHYZk3yiXW90A==:wDyl+WHB3yXWD1mGlCyfPvlzMuQjgWMUUZ4RFaLYIV5AGWhNK9iMGgGdIu/mTJL3Nw20EPcRUpGO4Og6Aa3NCwT6xg5l1kYvZsXcBF3UL+cDw15FGTi0q6KrmuaulL7Lib6RhX2I72T0TrqSyo18Q+Aa+eb27UdF8jkSf2rcuzWncSh9Te3mqzp9Uqr5+k1spDzgqcC4XeZzk7RHOyCbn7kPK63I6hW+qfXwQj6vwu4h6wrHQCXGuJAA7QtFmmCxVR/m6km9+s3Vp3sTpPSh1Xbed76hdobUn8CY9Fr/UOFr6yuvQA6VwrX1XKJAyBmF04yEIItV1l/92gkLXkysohUeM5V36cOVvyMwArwXAoENilO5oJlhugY9q7I6JxLNhHmaQcbLm8FUQ0p/11KL+hytj7U4JonvTdAJqay8TN5Vo8r/XsNzufDJUYDSW04nLwN+gNyQr0jU540c7dh3yTGw9655bwdoP90n240FSlLWVnfYa+nfkVY5WZv5LzSp:ZqbgFghmUOMklzAcgUegeFnjGTtMJe9QRJfJQv0um/o=",
            "ASP.NET_SessionId": "azdyuj5jbh4a0m2l0wx50gyd",
            "visid_incap_2271082": "bPBdanKrTzuM399rJFL7GO+X5WMAAAAAQUIPAAAAAAB2PTZ+Iok4pK97KpHNH2+W",
            "nlbi_2271082": "r2y4b+kZNm6JnW1bVPrQ3QAAAABQpn+aLwlKfBQC6/pFSNzB",
            "incap_ses_675_2271082": "X38ZL9hNen4mKmH+yxVeCe+X5WMAAAAAZrVVaJYQ4foUve3Y01g+jQ==",
            "nlbi_2269415_2147483392": "+XVDO3CFGRE/Grc7+0V6nQAAAADlPEJpUTl2cRYCfggXoDG0",
        }

        self.headers = {
            "authority": "api2.realtor.ca",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://www.realtor.ca",
            "referer": "https://www.realtor.ca/",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }

        self.data = {
            "ZoomLevel": "11",
            "LatitudeMax": "49.37425",
            "LongitudeMax": "-122.70782",
            "LatitudeMin": "49.14077",
            "LongitudeMin": "-123.53934",
            "Sort": "6-D",
            "PropertyTypeGroupID": "1",
            "PropertySearchTypeId": "0",
            "TransactionTypeId": "2",
            "Currency": "CAD",
            "RecordsPerPage": "12",
            "ApplicationId": "1",
            "CultureId": "1",
            "Version": "7.0",
            "CurrentPage": str(self.page),
        }

        # Call the next function to retrieve all the values
        self.post()
        result = self.response.json() if not self.err else self.err
        return result

    def post(self) -> None:
        """Send a POST request to get all the data from the website."""
        try:
            self.response = requests.post(
                "https://api2.realtor.ca/Listing.svc/PropertySearch_Post",
                cookies=self.cookies,
                headers=self.headers,
                data=self.data,
            )
        except Exception as error:
            self.err = str(error)


class PieChart:
    """
    Open a pie chart with the percentage of properties with 4 bedrooms.
    """

    def __init__(self, bedrooms: List) -> None:
        self.slices = []
        self.labels = []
        self.explode = []
        self.bedrooms = [int(v) for v in bedrooms]
        self.max_value = max(self.bedrooms)
        self.others = []
        self.colors = ["#50c878", "#febe10", "#ee82ee", "#ff8c00", "#00ccff"]

    def __call__(self) -> None:
        plt.style.use("fivethirtyeight")

        for i in range(1, self.max_value + 1):
            # Only 1 to 4 beds will be considered.
            if i < 5:
                self.slices.append(self.bedrooms.count(i))
                if i == 1:
                    self.labels.append(f"{i} Bed")
                else:
                    self.labels.append(f"{i} Beds")

                if i == 4:
                    self.explode.append(0.2)
                self.explode.append(0)
            # For all the props with more than 4 beds
            else:
                self.others.append(self.bedrooms.count(i))
        more_than_4 = sum(self.others)
        self.slices.append(more_than_4)
        self.labels.append("Others")
        plt.pie(
            self.slices,
            labels=self.labels,
            explode=self.explode,
            colors=self.colors,
            shadow=True,
            startangle=90,
            autopct="%1.1f%%",
            wedgeprops={"linewidth": 1.0, "edgecolor": "white"},
            textprops={"size": "small"},
        )
        plt.title("Number of Bedrooms", fontsize=18)
        plt.savefig("pie_chart_results.png")
        plt.tight_layout()
        plt.show()


class Scrapping:
    """
    Get all the web scrapping data and send to database.
    You can also save to excel and show a pie chart.
    """

    def __init__(self) -> None:
        self.bedrooms = []
        self.bathrooms = []
        self.address = []
        self.agent_name = []
        self.area_code = []
        self.phone_number = []
        self.price = []
        self.table = None
        self.engine = create_engine(
            "postgresql://postgres:postgres@0.0.0.0:5432/webscrappingdb"
        )

    def __call__(self) -> None:
        """Generate a table with the collected data from web scrapping."""
        for i in range(1, 51):
            # For visual purposes display a progress bar
            for t in tqdm(range(1), desc=f"Item_{i}", ascii=True, ncols=70):
                get_data = GetData(i)
                items = get_data()

                for item in items["Results"]:
                    try:
                        self.bathrooms.append(item["Building"]["BathroomTotal"])
                    except KeyError:
                        self.bathrooms.append("0")

                    try:
                        self.bedrooms.append(item["Building"]["Bedrooms"])
                    except KeyError:
                        self.bedrooms.append("0")

                    try:
                        self.address.append(item["Property"]["Address"]["AddressText"])
                    except KeyError:
                        self.address.append("Not Applicable")

                    try:
                        self.agent_name.append(item["Individual"][0]["Name"])
                    except KeyError:
                        self.agent_name.append("Not Applicable")

                    try:
                        self.area_code.append(
                            item["Individual"][0]["Phones"][0]["AreaCode"]
                        )
                    except KeyError:
                        self.area_code.append("Not Applicable")

                    try:
                        self.phone_number.append(
                            item["Individual"][0]["Phones"][0]["PhoneNumber"]
                        )
                    except KeyError:
                        self.phone_number.append("Not Applicable")

                    try:
                        self.price.append(item["Property"]["Price"])
                    except KeyError:
                        self.price.append("0")
        self.table = pd.DataFrame(
            {
                "Bathrooms": self.bathrooms,
                "Bedrooms": self.bedrooms,
                "Address": self.address,
                "Price": self.price,
                "Agent": self.agent_name,
                "Area Code": self.area_code,
                "Phone Number": self.phone_number,
            }
        )

        pie_chart = PieChart(self.bedrooms)
        self.send_to_psql()
        pie_chart()

    def save_to_excel(self) -> None:
        """Save data collected from web scrapping as an Excel file."""
        self.table.to_excel("web_scrapping.xlsx", index=0)

    def send_to_psql(self) -> str:
        """Send data collected from web scrapping to database."""
        try:
            self.table.to_sql("web_scrapping_results", self.engine, index=0)
        except Exception as err:
            print({"\nError": str(err)})
        else:
            print("\nDatabase Updated Successfully.\n")


if __name__ == "__main__":
    obj = Scrapping()
    obj()
