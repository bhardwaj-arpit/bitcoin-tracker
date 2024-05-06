import requests
from datetime import datetime


def fetch_bitcoin_data():
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        response.raise_for_status()  # Raise an error for unsuccessful HTTP responses
        data = response.json()
        price = data['bpi']['USD']['rate']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return price, current_time
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None


def generate_html(price, current_time, country):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bitcoin Price Tracker</title>
        <style>
            body {{
                background-color: blue;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            .container {{
                padding: 20px;
            }}
            canvas {{
                background-color: rgba(0, 0, 0, 0); /* Set canvas background color to transparent */
                display: block;
                margin: 0 auto;
                margin-top: 20px;
            }}
            #price {{
                font-size: 24px;
                margin-bottom: 10px;
            }}
            #refresh-button {{
                padding: 10px 20px;
                background-color: #00bfff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            #refresh-button:hover {{
                background-color: #0080ff;
            }}
            #marquee {{
                font-size: 18px;
                margin-top: 20px;
            }}
            #logo {{
                width: 150px;
                margin: 20px auto;
                display: block;
            }}
        </style>
        <!-- Include Chart.js library -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-1sLF508SXX2bSU4RmqLnIc6xEhF43vjcHA&usqp=CAU" alt="Logo" id="logo">
        <div class="container">
            <h1>Bitcoin Price Tracker</h1>
            <div id="price">Bitcoin Price: {price} USD | Current Time: {current_time} | Country: {country}</div>
            <button id="refresh-button" onclick="refreshData()">Refresh Data</button>
            <canvas id="bitcoinChart" width="600" height="300"></canvas>
            <marquee id="marquee">Bitcoin Price: {price} USD | Current Time: {current_time}</marquee>
        </div>
        <script>
            function refreshData() {{
                window.location.reload();
            }}
            // JavaScript code for fetching Bitcoin price history and drawing chart
            fetch('https://api.coindesk.com/v1/bpi/historical/close.json')
                .then(response => response.json())
                .then(data => {{
                    const dates = Object.keys(data.bpi);
                    const prices = Object.values(data.bpi);
                    // Get canvas element
                    const ctx = document.getElementById('bitcoinChart').getContext('2d');
                    // Create new chart object
                    const chart = new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: dates,
                            datasets: [{{
                                label: 'Bitcoin Price (USD)',
                                data: prices,
                                backgroundColor: 'yellow', // Background color (yellow)
                                borderColor: 'black',     // Border color (black)
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            scales: {{
                                y: {{
                                    beginAtZero: false
                                }}
                            }},
                            plugins: {{
                                legend: {{
                                    labels: {{
                                        font: {{
                                            size: 14,
                                            weight: 'bold'
                                        }},
                                        color: 'white'
                                    }}
                                }}
                            }}
                        }}
                    }});
                }})
                .catch(error => console.error('Error fetching data:', error));
        </script>
    </body>
    </html>
    """
    return html_content


def main():
    price, current_time = fetch_bitcoin_data()
    if price is not None and current_time is not None:
        # Dummy data for country (replace with actual data)
        country = "India"

        html_content = generate_html(price, current_time, country)
        with open("bitcoin_price_tracker.html", "w") as html_file:
            html_file.write(html_content)
        print("HTML file generated successfully.")
    else:
        print("Failed to fetch Bitcoin data.")


if __name__ == "__main__":
    main()
