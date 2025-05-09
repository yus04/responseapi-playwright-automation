import asyncio
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, AZURE_OPENAI_MODEL, ITERATIONS, HEADLESS
from action import handle_action, take_screenshot

async def process_model_response(client, response, page, max_iterations=ITERATIONS):
    """Process the model's response and execute actions."""
    for iteration in range(max_iterations):
        if not hasattr(response, 'output') or not response.output:
            print("No output from model.")
            break
        
        # Safely access response id
        response_id = getattr(response, 'id', 'unknown')
        print(f"\nIteration {iteration + 1} - Response ID: {response_id}\n")
        
        # Print text responses and reasoning
        for item in response.output:
            # Handle text output
            if hasattr(item, 'type') and item.type == "text":
                print(f"\nModel message: {item.text}\n")
                
            # Handle reasoning output
            if hasattr(item, 'type') and item.type == "reasoning":
                # Extract meaningful content from the reasoning
                meaningful_content = []
                
                if hasattr(item, 'summary') and item.summary:
                    for summary in item.summary:
                        # Handle different potential formats of summary content
                        if isinstance(summary, str) and summary.strip():
                            meaningful_content.append(summary)
                        elif hasattr(summary, 'text') and summary.text.strip():
                            meaningful_content.append(summary.text)
                
                # Only print reasoning section if there's actual content
                if meaningful_content:
                    print("=== Model Reasoning ===")
                    for idx, content in enumerate(meaningful_content, 1):
                        print(f"{content}")
                    print("=====================\n")
        
        # Extract computer calls
        computer_calls = [item for item in response.output 
                         if hasattr(item, 'type') and item.type == "computer_call"]
        
        if not computer_calls:
            print("No computer call found in response. Reverting control to human supervisor")
            break
        
        computer_call = computer_calls[0]
        if not hasattr(computer_call, 'call_id') or not hasattr(computer_call, 'action'):
            print("Computer call is missing required attributes.")
            break
        
        call_id = computer_call.call_id
        action = computer_call.action
        
        # Handle safety checks
        acknowledged_checks = []
        if hasattr(computer_call, 'pending_safety_checks') and computer_call.pending_safety_checks:
            pending_checks = computer_call.pending_safety_checks

            if not HEADLESS:
                print("\nSafety checks required:")
                for check in pending_checks:
                    print(f"- {check.code}: {check.message}")
                
                if input("\nDo you want to proceed? (y/n): ").lower() != 'y':
                    print("Operation cancelled by user.")
                    break
            
            acknowledged_checks = pending_checks
        
        # Execute the action
        try:
           await page.bring_to_front()
           await handle_action(page, action)
           
           # Check if a new page was created after the action
           if action.type in ["click"]:
               await asyncio.sleep(1.5)
               # Get all pages in the context
               all_pages = page.context.pages
               # If we have multiple pages, check if there's a newer one
               if len(all_pages) > 1:
                   newest_page = all_pages[-1]  # Last page is usually the newest
                   if newest_page != page and newest_page.url not in ["about:blank", ""]:
                       print(f"\tSwitching to new tab: {newest_page.url}")
                       page = newest_page  # Update our page reference
           elif action.type != "wait":
               await asyncio.sleep(0.5)
               
        except Exception as e:
           print(f"Error handling action {action.type}: {e}")
           import traceback
           traceback.print_exc()    

        # Take a screenshot after the action
        screenshot_base64 = await take_screenshot(page)

        print("\tNew screenshot taken")
        
        # Prepare input for the next request
        input_content = [{
            "type": "computer_call_output",
            "call_id": call_id,
            "output": {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{screenshot_base64}"
            }
        }]
        
        # Add acknowledged safety checks if any
        if acknowledged_checks:
            acknowledged_checks_dicts = []
            for check in acknowledged_checks:
                acknowledged_checks_dicts.append({
                    "id": check.id,
                    "code": check.code,
                    "message": check.message
                })
            input_content[0]["acknowledged_safety_checks"] = acknowledged_checks_dicts
        
        # Add current URL for context
        try:
            current_url = page.url
            if current_url and current_url != "about:blank":
                input_content[0]["current_url"] = current_url
                print(f"\tCurrent URL: {current_url}")
        except Exception as e:
            print(f"Error getting URL: {e}")
        
        # Send the screenshot back for the next step
        try:
            response = client.responses.create(
                model=AZURE_OPENAI_MODEL,
                previous_response_id=response_id,
                tools=[{
                    "type": "computer_use_preview",
                    "display_width": DISPLAY_WIDTH,
                    "display_height": DISPLAY_HEIGHT,
                    "environment": "browser"
                }],
                input=input_content,
                truncation="auto"
            )

            print("\tModel processing screenshot")
        except Exception as e:
            print(f"Error in API call: {e}")
            import traceback
            traceback.print_exc()
            break
    
    if iteration >= max_iterations - 1:
        print("Reached maximum number of iterations. Stopping.")
