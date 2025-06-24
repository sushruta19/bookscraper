import os

def create_env_file():
    print("Please provide the following database credentials:")

    MYSQL_HOST = input("Enter MySQL host (e.g., localhost): ")
    MYSQL_USER = input("Enter MySQL username(e.g., root): ")
    MYSQL_PASSWORD = input("Enter MySQL password: ")
    MYSQL_DATABASE = input("Enter MySQL database name: ")
    print("\n\nPlease go to https://scrapeops.io/app/register/main/ to get fake Browser-Agents and paste your API Key here below...")
    SCRAPEOPS_API_KEY = input("Enter your Scrapeops API Key: ")

    env_content = f"""
MYSQL_HOST={MYSQL_HOST}
MYSQL_USER={MYSQL_USER}
MYSQL_PASSWORD={MYSQL_PASSWORD}
MYSQL_DATABASE={MYSQL_DATABASE}
SCRAPEOPS_API_KEY={SCRAPEOPS_API_KEY}
    """
    env_file_path = os.path.join(os.getcwd(), "bookscraper", "bookscraper", ".env")
    with open(env_file_path, "w") as file:
        file.write(env_content)
    
    print(f".env file created successfully at {env_file_path}")
    print("\nNext Steps:")
    print("1)Make sure your MySQL server is running.")
    print("2)Confirm the database exists (or create it).")
    print("3)Activate your virtual environment")
    print("\nIf you don’t have a virtual environment yet:")
    print("For Windows (CMD):")
    print("    python -m venv venv")
    print("    venv\\Scripts\\activate")
    print("For Linux or Mac:")
    print("    python3 -m venv venv")
    print("    source venv/bin/activate")

    print("\nOnce inside the virtual environment:")
    print("1) Install required packages:")
    print("    pip install -r requirements.txt")
    print("\n2) Move to the main Scrapy project directory:")
    print("    cd bookscraper")
    print("\n3) To see available spiders:")
    print("    scrapy list")
    print("4) To run the spider:")
    print("    scrapy crawl bookspider")
    print("\n5) To export the output to a file (JSON/CSV):")
    print("    scrapy crawl bookspider -O output.json")
    print("    scrapy crawl bookspider -O output.csv")
    print("\nYou can inspect the SQL data directly in your MySQL DB.")

if __name__ == "__main__":
    create_env_file()