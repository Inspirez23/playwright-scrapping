from playwright.sync_api import sync_playwright
import ollama

def get_mlb_headlines():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)  # Launches a headless Chromium browser
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.mlb.com/news/")
        page.wait_for_load_state("load")

        # Extract specific element's text
        h1_elements = page.query_selector_all("h1")
        headlines = [element.text_content() for element in h1_elements]
        
        browser.close()
        return headlines

def generate_natural_language_summary():
    headlines = get_mlb_headlines()
    headlines_text = "\n".join(headlines)
    
    try:
        response = ollama.chat(model="gemma3:4b", messages=[{"role": "user", "content": f"Summarize the following MLB headlines in natural language:\n{headlines_text}"}])
        summary = response.get("message", "No response received from the model.")
        print("Natural Language Summary:")
        print(summary)
    except Exception as e:
        print("Error generating summary:", str(e))

print(get_mlb_headlines())

if __name__ == "__main__":
    generate_natural_language_summary()
