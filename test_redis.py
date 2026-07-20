import os
import redis
from dotenv import load_dotenv

# Load the local .env file
load_dotenv()

# Get the REDIS_URL from the .env file
redis_url = os.getenv("REDIS_URL")

print(f"Testing URL: {redis_url}")

if not redis_url:
    print("❌ ERROR: REDIS_URL is not found in your .env file.")
else:
    try:
        # Try connecting to Redis
        client = redis.from_url(redis_url, decode_responses=True)
        # Send a basic PING command to verify credentials
        response = client.ping()
        
        if response:
            print("✅ SUCCESS! Your Redis connection works perfectly.")
            print("You can now safely paste this exact URL into your Render Environment Variables.")
    except redis.exceptions.AuthenticationError:
        print("❌ ERROR: Invalid username-password pair. You are still using the REST token instead of the real password.")
    except Exception as e:
        print(f"❌ ERROR: Could not connect. Details: {e}")
