import asyncio
import time

async def fetch_weather(city):
    print(f"Fetching weather for {city}...")
    await asyncio.sleep(2)  # Simulate network delay
    print(f"{city} done!")
    return f"Weather data for {city}"   
async def main():
    cities = ["Helsinki", "Tehran", "London"]
    
    start_time = time.perf_counter()
    
    tasks = [fetch_weather(city) for city in cities]
    
    results = await asyncio.gather(*tasks)
    
    print(f"Results: {results}")
    
    end_time = time.perf_counter()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

def fetch_weather_sync(city):
    print(f"Fetching weather for {city}...")
    time.sleep(2)  # Simulate network delay
    print(f"{city} done!")
    return f"Weather data for {city}"

def main_sync():
    cities = ["Helsinki", "Tehran", "London"]
    
    start_time = time.perf_counter()
    
    results = [fetch_weather_sync(city) for city in cities]
    
    print(f"Results: {results}")
    
    end_time = time.perf_counter()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    print("Running synchronous version:")
    main_sync()
    
    print("\nRunning asynchronous version:")
    asyncio.run(main())













# 2. Create a new file called 'async_demo.py':
#    - Fetch weather for Helsinki, Tehran, London
#      ALL AT THE SAME TIME using asyncio.gather()
#    - Compare with sync version
#    - Print how long each version takes!