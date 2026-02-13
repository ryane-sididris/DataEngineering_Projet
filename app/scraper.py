from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pymongo
import time

def run_scraper():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://pokemondb.net/pokedex/all")
        time.sleep(2) 
        
        rows = driver.find_elements(By.CSS_SELECTOR, "table#pokedex tbody tr")
        
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            
            gray_text = row.find_elements(By.CSS_SELECTOR, ".text-muted")
            if gray_text:
                name = gray_text[0].text
            else:
                name = row.find_elements(By.CSS_SELECTOR, ".ent-name")[0].text
            
            icon = row.find_elements(By.CSS_SELECTOR, ".img-fixed")
            if icon:
                icon_src = icon[0].get_attribute("data-src")
                if not icon_src:
                    icon_src = icon[0].get_attribute("src")
                slug = icon_src.split("/")[-1].replace(".png", "")
                img_url = f"https://img.pokemondb.net/artwork/large/{slug}.jpg"
            else:
                img_url = "https://img.pokemondb.net/artwork/large/bulbasaur.jpg"

            pokemon = {
                "id": cols[0].text,
                "nom": name,
                "type": cols[2].text.split("\n")[0],
                "total": int(cols[3].text),
                "hp": int(cols[4].text),
                "attaque": int(cols[5].text),
                "defense": int(cols[6].text),
                "image": img_url
            }
            data.append(pokemon)

        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        db = client["pokedex_db"]
        collection = db["pokemons"]
        
        collection.delete_many({})
        if data:
            collection.insert_many(data)
        
        return len(data)

    except Exception:
        return 0
    
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()