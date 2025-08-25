import requests
from datetime import date, timedelta


def fetch_and_loop_weather_data():
    """
    Fetches weather data for the last 7 days (excluding today),
    and prints Date, Max Temp, and Min Temp. Shows 'None' where data is missing.
    Includes detailed error handling and messages.
    """
    latitude = 17.38
    longitude = 78.48
    today = date.today()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    api_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}&"
        f"start_date={start_date}&end_date={end_date}&"
        f"daily=temperature_2m_max,temperature_2m_min"
    )

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        data = response.json()

        daily_data = data.get("daily", {})
        dates = daily_data.get("time", [])
        max_temps = daily_data.get("temperature_2m_max", [])
        min_temps = daily_data.get("temperature_2m_min", [])

        print(f"\n{'Date':<12} {'Max Temp (°C)':<15} {'Min Temp (°C)':<15}")
        print("-" * 45)

        for single_date, max_temp, min_temp in zip(dates, max_temps, min_temps):
            max_str = str(max_temp) if max_temp is not None else "None"
            min_str = str(min_temp) if min_temp is not None else "None"
            print(f"{single_date} {max_str} {min_str}")
            #print(f"{single_date:<12} {max_str:<15} {min_str:<15}")
        max_temp_total=[x for x in max_temps if x is not None]
        if max_temp_total:
            highest_max_temp=max(max_temp_total)
            print(f"\nHighest temperature recorded in last 7 days: {highest_max_temp}°C")
        else:
            print("\nNo valid maximum temperature data available for the last 7 days.")
        min_temp_total= [x for x in min_temps if x is not None]
        if min_temp_total:
            lowest_max_temp = min(min_temp_total)
            print(f"\nLowest temperature recorded in last 7 days: {lowest_max_temp}°C")
        else:
            print("\nNo valid Minimum temperature data available for the last 7 days.")
    except requests.exceptions.HTTPError as err:
        print(f"\n❌ HTTP error occurred: {err}")
        try:
            error_detail = response.json()
            print("🔎 API response:", error_detail)
        except ValueError:
            print("⚠️ No JSON body in error response.")

    except requests.exceptions.ConnectionError as err:
        print(f"\n❌ Connection error: {err}")

    except requests.exceptions.Timeout as err:
        print(f"\n⏳ Request timed out: {err}")

    except requests.exceptions.RequestException as err:
        print(f"\n⚠️ General request error: {err}")

    except Exception as err:
        print(f"\n🔥 Unexpected error: {err}")


if __name__ == "__main__":
    fetch_and_loop_weather_data()
