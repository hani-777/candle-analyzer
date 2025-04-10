# Candle Analyzer

A lightweight Python tool to analyze candlestick behavior using MetaTrader 5 data. This script generates detailed statistical insights about candle pattern transitions (e.g., Red to Green, Green to Red, etc.) and exports the results as both a CSV file and an interactive HTML report with charts.

## 🔍 What It Does

- Connects to MetaTrader 5 and fetches M1 timeframe data for a specified symbol
- Calculates four key pattern transitions:
  - Red to Green (reversal)
  - Red to Red (bearish continuation)
  - Green to Red (reversal)
  - Green to Green (bullish continuation)
- Aggregates results by day
- Exports:
  - `candle_analysis.csv`: raw statistics
  - `candle_analysis.html`: full report with interactive bar chart and summaries

## 📦 Requirements

Install the following Python packages:

```bash
pip install MetaTrader5 pandas pytz
```

## 🛠️ How to Use

1. Make sure MetaTrader 5 is installed and running.
2. Open your terminal and run the script:

```bash
python candle_analyzer.py
```

3. After execution, you'll find:
   - `candle_analysis.csv` – the raw output
   - `candle_analysis.html` – the visual report

## 📈 Example Output

![Bar Chart Example](./example_output/candle_analysis_example.png)

## 💡 Why This Is Useful

Most traders assume candle colors predict the next move, but this tool shows the real statistical behavior behind candles. It helps verify strategies with real data instead of gut feeling.

## 🔗 More Info

Visit [hani.solutions](https://hani.solutions) for updates, examples, and support.

## 📄 License

This project is licensed under the MIT License – feel free to use or modify with credit.
