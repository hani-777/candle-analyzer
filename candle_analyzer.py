import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

def save_to_csv(stats_df, filename="candle_analysis.csv"):
    """Save the analysis results to a CSV file"""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create full path for the CSV file
    csv_path = os.path.join(script_dir, filename)
    stats_df.to_csv(csv_path, index=False)
    print(f"\nAnalysis saved to {csv_path}")

def create_html_report(stats_df, filename="candle_analysis.html"):
    """Create an HTML report with formatted tables and styling"""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create full path for the HTML file
    html_path = os.path.join(script_dir, filename)
    
    # Calculate overall statistics
    total_candles = stats_df['total_candles'].sum()
    avg_red_to_green = stats_df['red_to_green_percent'].mean()
    avg_red_to_red = stats_df['red_to_red_percent'].mean()
    avg_green_to_red = stats_df['green_to_red_percent'].mean()
    avg_green_to_green = stats_df['green_to_green_percent'].mean()
    
    # Create the HTML content with proper string formatting
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Candlestick Pattern Analysis</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .summary {{ margin-top: 20px; padding: 15px; background-color: #f0f8ff; }}
            .date {{ font-weight: bold; }}
            .percentage {{ color: #0066cc; }}
            .chart-container {{ width: 80%; margin: 20px auto; }}
            .analysis-section {{ margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 5px; }}
            .highlight {{ color: #28a745; font-weight: bold; }}
            .warning {{ color: #dc3545; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Candlestick Pattern Analysis Report,... for more info visit <a href="https://hani.solutions">Hani.solutions</a></h1>
        <div class="summary">
            <h2>Summary</h2>
            <p>Analysis Period: {stats_df['date'].min()} to {stats_df['date'].max()}</p>
            <p>Total Days Analyzed: {len(stats_df)}</p>
            <p>Average Candles per Day: {stats_df['total_candles'].mean():.0f}</p>
        </div>
    """

    # Add daily analysis tables
    for _, row in stats_df.iterrows():
        html_content += f"""
        <h2>Analysis for {row['date']}</h2>
        <table>
            <tr>
                <th>Pattern</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
            <tr>
                <td>Red to Green</td>
                <td>{row['red_to_green']}</td>
                <td class="percentage">{row['red_to_green_percent']:.2f}%</td>
            </tr>
            <tr>
                <td>Red to Red</td>
                <td>{row['red_to_red']}</td>
                <td class="percentage">{row['red_to_red_percent']:.2f}%</td>
            </tr>
            <tr>
                <td>Green to Red</td>
                <td>{row['green_to_red']}</td>
                <td class="percentage">{row['green_to_red_percent']:.2f}%</td>
            </tr>
            <tr>
                <td>Green to Green</td>
                <td>{row['green_to_green']}</td>
                <td class="percentage">{row['green_to_green_percent']:.2f}%</td>
            </tr>
            <tr>
                <td><strong>Total Candles</strong></td>
                <td colspan="2"><strong>{row['total_candles']}</strong></td>
            </tr>
        </table>
        """

    # Add overall analysis section
    html_content += f"""
        <div class="analysis-section">
            <h2>Overall Analysis</h2>
            <div class="chart-container">
                <canvas id="patternChart"></canvas>
            </div>
            <h3>Key Findings:</h3>
            <ul>
                <li>Average Red to Green transitions: <span class="percentage">{avg_red_to_green:.2f}%</span></li>
                <li>Average Red to Red continuations: <span class="percentage">{avg_red_to_red:.2f}%</span></li>
                <li>Average Green to Red transitions: <span class="percentage">{avg_green_to_red:.2f}%</span></li>
                <li>Average Green to Green continuations: <span class="percentage">{avg_green_to_green:.2f}%</span></li>
            </ul>
            <h3>Market Behavior Analysis:</h3>
            <p>Based on the data analysis:</p>
            <ul>
                <li>{"<span class='highlight'>Strong trend continuation</span>" if avg_red_to_red > 25 or avg_green_to_green > 25 else "<span class='warning'>Weak trend continuation</span>"} - The market shows {"strong" if avg_red_to_red > 25 or avg_green_to_green > 25 else "weak"} tendency to continue existing trends</li>
                <li>{"<span class='highlight'>High reversal probability</span>" if avg_red_to_green > 25 or avg_green_to_red > 25 else "<span class='warning'>Low reversal probability</span>"} - The market shows {"high" if avg_red_to_green > 25 or avg_green_to_red > 25 else "low"} probability of trend reversals</li>
                <li>{"<span class='highlight'>Balanced market</span>" if abs(avg_red_to_red - avg_green_to_green) < 5 else "<span class='warning'>Unbalanced market</span>"} - The market shows {"balanced" if abs(avg_red_to_red - avg_green_to_green) < 5 else "unbalanced"} behavior between bullish and bearish movements</li>
            </ul>
        </div>

        <script>
            const ctx = document.getElementById('patternChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Red to Green', 'Red to Red', 'Green to Red', 'Green to Green'],
                    datasets: [{{
                        label: 'Average Percentage',
                        data: [{avg_red_to_green:.2f}, {avg_red_to_red:.2f}, {avg_green_to_red:.2f}, {avg_green_to_green:.2f}],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(75, 192, 192, 0.6)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: 'Percentage (%)'
                            }}
                        }}
                    }},
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Average Pattern Distribution'
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML report saved to {html_path}")

def analyze_candles(symbol="EURUSD"):
    # Initialize MT5
    if not mt5.initialize():
        print("Failed to initialize MT5")
        return
    
    # Set timezone to UTC
    timezone = pytz.timezone("Etc/UTC")
    
    # Calculate date range (one month ago)
    end_date = datetime.now(timezone)
    start_date = end_date - timedelta(days=50)
    
    # Get candlestick data
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, start_date, end_date)
    
    if rates is None:
        print("Failed to get rates")
        mt5.shutdown()
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Add color column (1 for green, -1 for red)
    df['color'] = df.apply(lambda x: 1 if x['close'] > x['open'] else -1, axis=1)
    
    # Add previous color column
    df['prev_color'] = df['color'].shift(1)
    
    # Group by date
    df['date'] = df['time'].dt.date
    
    # Calculate daily statistics
    daily_stats = []
    
    for date, group in df.groupby('date'):
        total_candles = len(group)
        red_to_green = len(group[(group['prev_color'] == -1) & (group['color'] == 1)])
        red_to_red = len(group[(group['prev_color'] == -1) & (group['color'] == -1)])
        green_to_red = len(group[(group['prev_color'] == 1) & (group['color'] == -1)])
        green_to_green = len(group[(group['prev_color'] == 1) & (group['color'] == 1)])
        
        daily_stats.append({
            'date': date,
            'total_candles': total_candles,
            'red_to_green': red_to_green,
            'red_to_red': red_to_red,
            'green_to_red': green_to_red,
            'green_to_green': green_to_green,
            'red_to_green_percent': (red_to_green / total_candles) * 100 if total_candles > 0 else 0,
            'red_to_red_percent': (red_to_red / total_candles) * 100 if total_candles > 0 else 0,
            'green_to_red_percent': (green_to_red / total_candles) * 100 if total_candles > 0 else 0,
            'green_to_green_percent': (green_to_green / total_candles) * 100 if total_candles > 0 else 0
        })
    
    # Convert to DataFrame
    stats_df = pd.DataFrame(daily_stats)
    
    # Save results
    save_to_csv(stats_df)
    create_html_report(stats_df)
    
    # Shutdown MT5
    mt5.shutdown()

if __name__ == "__main__":
    analyze_candles()
