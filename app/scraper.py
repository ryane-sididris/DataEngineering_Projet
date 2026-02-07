from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pymongo
import time

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["pokedex_db"]
collection = db["pokemons"]

def run_scraper():
    print("Starting Scraper...")
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://pokemondb.net/pokedex/all")
        time.sleep(2)

        data = []
        rows = driver.find_elements(By.CSS_SELECTOR, "table#pokedex tbody tr")
        
        for row in rows[:151]: # Gen 1 only
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                
                name = cols[1].find_element(By.CSS_SELECTOR, "a.ent-name").text
                slug = name.lower().replace(" ", "-").replace(".", "").replace("'", "").replace("♀", "-f").replace("♂", "-m")
                
                types = [t.text for t in cols[2].find_elements(By.CSS_SELECTOR, "a")]
                
                data.append({
                    "nom": name,
                    "type": types[0],
                    "total": int(cols[3].text),
                    "hp": int(cols[4].text),
                    "attaque": int(cols[5].text),
                    "defense": int(cols[6].text),
                    "vitesse": int(cols[9].text),
                    "image": f"https://img.pokemondb.net/artwork/{slug}.jpg"
                })
            except:
                continue

        if data:
            collection.delete_many({}) 
            collection.insert_many(data)
            print(f"Success: {len(data)} pokemon added.")
        
        return len(data)

    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()