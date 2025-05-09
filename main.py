import asyncio
from openai import AzureOpenAI
from playwright.async_api import async_playwright
from auth import get_token_provider
from process import process_model_response
from action import take_screenshot, save_local_screenshot
from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_MODEL, DISPLAY_WIDTH, DISPLAY_HEIGHT, AZURE_OPENAI_API_VERSION, WEB_URL, HEADLESS, INSTRUCTIONS
        
async def main():    
    # Initialize OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_ad_token_provider=get_token_provider(),
        api_version=AZURE_OPENAI_API_VERSION
    )
    
    # Initialize Playwright
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=HEADLESS,
            args=[f"--window-size={DISPLAY_WIDTH},{DISPLAY_HEIGHT}", "--disable-extensions"]
        )
        
        context = await browser.new_context(
            viewport={"width": DISPLAY_WIDTH, "height": DISPLAY_HEIGHT},
            accept_downloads=True
        )
        
        page = await context.new_page()
        
        # Navigate to starting page
        await page.goto(WEB_URL, wait_until="domcontentloaded")
        print(f"Browser initialized to {WEB_URL}")
        
        # Main interaction loop
        try:
            while True:
                print("\n" + "="*50)
                if not HEADLESS:
                    user_input = input("Enter a task to perform (or 'exit' to quit): ")
                else:
                    user_input = "プロンプトに従って、ブラウザを操作してください。"
                    print(f"User input: {user_input}")
                
                if user_input.lower() in ('exit', 'quit'):
                    break
                
                if not user_input.strip():
                    continue
                
                # Take initial screenshot
                screenshot_base64 = await take_screenshot(page)
                print("\nTake initial screenshot")
                
                # Initial request to the model
                response = client.responses.create(
                    model=AZURE_OPENAI_MODEL,
                    tools=[{
                        "type": "computer_use_preview",
                        "display_width": DISPLAY_WIDTH,
                        "display_height": DISPLAY_HEIGHT,
                        "environment": "browser"
                    }],
                    instructions = INSTRUCTIONS,
                    input=[{
                        "role": "user",
                        "content": [{
                            "type": "input_text",
                            "text": user_input
                        }, {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{screenshot_base64}"
                        }]
                    }],
                    reasoning={"generate_summary": "concise"},
                    truncation="auto"
                )
                print("\nSending model initial screenshot and instructions")

                # Process model actions
                await process_model_response(client, response, page)

                if HEADLESS:
                    # exit the loop
                    break
                
        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if HEADLESS:
                # Save final screenshot before closing the browser
                await save_local_screenshot(page, "output/final_screenshot.png")

            # Close browser
            await context.close()
            await browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
