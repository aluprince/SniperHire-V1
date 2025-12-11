import os
from .utils.logger import logger
import re
from dotenv import load_dotenv, find_dotenv
import asyncio
from playwright.async_api import async_playwright, Playwright, TimeoutError as PlaywrightTimeoutError
from ...db.models import JobScraped
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


load_dotenv(find_dotenv())

JOBBERMAN_EMAIL = os.getenv("JOBBERMAN_EMAIL")
JOBBERMAN_PASSWORD = os.getenv("JOBBERMAN_PASSWORD")



async def scrape_jobberman_job(playwright: Playwright, job_title: str, locations: str, num_of_jobs: int, lastest_only: bool, db:Session):
    try:
        logger.info(">>> LET TRY JOBBERMAN JOBBOARD TODAY")
        logger.info(">>> LOGGER ACTIVE")
        url = "https://www.jobberman.com/account/login"
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = await chromium.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(100000)

        await page.goto(url)
        await asyncio.sleep(5)
        

        # Handle cookie modal
        try:
            cookie_btn = page.locator("#onetrust-accept-btn-handler")
            if await cookie_btn.is_visible():
                await cookie_btn.click()
                await page.wait_for_timeout(500)
        except:
            pass

        # First Login to the JobSite

        try:

            await page.get_by_placeholder("Email Address").fill(JOBBERMAN_EMAIL)
            await page.get_by_placeholder("Password").fill(JOBBERMAN_PASSWORD)

            login_button = page.get_by_role("button", name="Log in")
            await login_button.click()

            await page.wait_for_load_state("networkidle")
            logger.info(">>> LOGIN SUCCESSFULLY >>>")

            await asyncio.sleep(5)
        except Exception as e:
            logger.debug(e)

        # Search for job
        try:
            logger.info(f">>>we are currently searching for your job: {job_title} roles...")
            print("hold on")
            search_job_btn = page.get_by_role("button", name="Find a job")
            if await search_job_btn.is_visible():
                await search_job_btn.click()
                await page.wait_for_timeout(500)
                await asyncio.sleep(5)
                # Get search box and fill job 
                search_box = page.get_by_placeholder("Search for Jobs")
                await search_box.fill(job_title)
                await search_box.click()

                # Actually search for the job 
                await search_box.press("Enter")
                jobs_available = page.locator("xpath=/html/body/main/section/div[3]/div[2]/div[1]/div[1]/div/span/span")
                current_jobs = await jobs_available.text_content()
                logger.info(f">>>we have currently seen {current_jobs} {job_title} roles")
        except Exception as e :
            logger.debug(e)

        #slow the scraper for some time
        await asyncio.sleep(5)

        # Filter by location
        try:
            print(">>>filtering by your current location")
            if locations.lower() == "remote":
                print(f">>>filtering by {locations.lower()}")
                print(f"Searcing for {job_title} roles with this locations: {locations.lower()}")
                location_btn = page.locator("xpath=/html/body/main/section/div[3]/div[2]/div[2]/div[2]/section/aside/div/form/div[4]/button")
                await location_btn.click() 

                location_box = page.locator("#opt-location-remote-label")
                await location_box.click()

                jobs_available_loc = page.locator("xpath=/html/body/main/section/div[3]/div[2]/div[1]/div[1]/div/span/span")
                current_jobs_loc = await jobs_available_loc.text_content()
                print(f"successfully filtered by {locations.lower()} locations..")
                print(f"current jobs when filtered by {locations.lower()} locations: {current_jobs_loc}")
            else:
                # TODO: work on robust locations
                pass
        except Exception as e:
            print("Error on filtering by location:", e)

        try:
            if lastest_only == True:
                lastest_block = page.locator("#opt-sort-latest-label")
                await lastest_block.click()
                await page.wait_for_load_state("networkidle")
        except Exception as e:
            print("Error filtering by lastest jobs", e)

        try:
            print(">>> scraping jobs now >>>")
            job_cards = page.locator("[data-cy='listing-cards-components']")
            count = await job_cards.count() #Job cards available
            print(count)

            if count == 0:
                raise Exception("===== Sorry no job found =====")
            
            limit = min(num_of_jobs, count)

            for i in range(limit):
                print(i)
                job_card = job_cards.nth(i) 
                card_text = await job_cards.nth(i).inner_text()
                print(job_card)
                card_btn = job_card.locator("p.text-lg") 
                await card_btn.click()

                try:
                    job_title = await page.locator("[data-cy='title-job']").inner_text()
                except:
                    job_title = "N/A"
                try:
                    job_company = await page.locator("h2 a.text-link-500").inner_text()
                except:
                        job_company = "N/A"
                try:
                    job_description = await page.locator("ul.list-disc.list-inside").all_inner_texts()
                except:
                    job_description = "N/A"
                print("job_title: ", job_title.strip())
                print("company: ", job_company.strip())
                print("description :",job_description)
                    
                print("card found:",  card_text)



                # Save to DB
                try:
                    new_job = JobScraped(
                        job_title=job_title,
                        job_company=job_company,
                        job_description=job_description,
                        location=locations
                    )
                    db.add(new_job)
                    db.commit()
                    db.refresh()
                except IntegrityError:
                    db.rollback()
                except Exception as e:
                    db.rollback()

                logger.info(f">>> {job_title} has been saved successfully to database ")

                await page.go_back()
        except Exception as e:
            logger.debug(e)       
       
    except TimeoutError:
        logger.debug("Timeout", TimeoutError)
    except Exception as e:
        logger.debug(e)
        print(">>>Scraper Failed.....")
    finally:
        await browser.close()
        logger.info(">>> BROWSER CLOSED >>>")

async def main():
    async with async_playwright() as playwright:
        await scrape_jobberman_job(playwright, "backend developer", "remote", 10, lastest_only=True)

if __name__ == "__main__":
    print(">>> starting >>>")
    asyncio.run(main())



