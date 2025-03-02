import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
       api_key=os.environ.get("ANTHROPIC_API_KEY")
   )

def generate_financial_summary(ticker, instrument_type):
    """
    Generate a beginner-friendly summary of a financial instrument using Claude.
    
    Args:
        ticker (str): The ticker symbol (e.g., 'AAPL', 'SPY')
        instrument_type (str): One of 'stock', 'index', 'etf', 'derivative', or 'bond'
    
    Returns:
        str: A beginner-friendly summary
    """
    # Crafts prompt for instrument type using base prompt
    base_prompt = """
        You are a helpful financial advisor explaining concepts to beginners.
        Please provide a beginner-friendly summary of {concept}.
        {specific_instructions}
        After the summary, give a brief example using the company with the ticker {ticker}. Keep explanations simple, beginner-friendly and avoid complex financial jargon.
    """
    
    specific_instructions = {
        'stock': f"Include why companies issue stocks, why people invest in stocks, basic metrics for beginners, and risks to consider.",
        'index':f"Include what an index is, why investors follow indices, basic information for beginners.",
        'etf': f"Include what an etf is, why investors invest in etfs, why etfs are good tools for beginners, and risks to consider.",
        'derivative': f"Include what a derivative is, why investors invest in derivatives, and why derivatives are risky tools for beginners.",
        'bond': f"Include what a bond is, why companies/governments/etc. issue bonds, why investors invest in bonds, and risks to consider.",
    }
    
    # Check if the instrument type is valid
    if instrument_type.lower() not in specific_instructions:
        return f"Error: '{instrument_type}' is not a supported financial instrument type. Please choose from: stock, index, etf, derivative, or bond."
    
    # Get the appropriate prompt
    prompt = base_prompt.format(concept=instrument_type.lower(), specific_instructions=specific_instructions[instrument_type.lower()], ticker=ticker)
    
    # Call Claude API
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        temperature=0.3,
        system="You are a helpful, accurate financial advisor who explains concepts simply to beginners.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def main():
    print("Welcome to Financial Concepts Explainer!")
    print("This tool helps beginners understand financial instruments.")
    print("\nAvailable financial instrument types:")
    print("1. Stocks - Individual company shares (e.g., AAPL, MSFT)")
    print("2. Indexes - Market benchmarks (e.g., SPX, DJI)")
    print("3. ETFs - Exchange-Traded Funds (e.g., SPY, QQQ)")
    print("4. Derivatives - Options, futures, etc. (e.g., specific contracts)")
    print("5. Bonds - Debt securities (e.g., Treasury bonds, corporate bonds)")
    
    while True:
        # Get user input
        ticker = input("\nEnter a ticker symbol (or 'quit' to exit): ").strip().upper()
        if ticker.lower() == 'quit':
            break
        
        # Get instrument type
        print("\nSelect the type of financial instrument:")
        print("1: Stock")
        print("2: Index")
        print("3: ETF")
        print("4: Derivative")
        print("5: Bond")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        # Map the choice to instrument type
        type_map = {
            '1': 'stock',
            '2': 'index',
            '3': 'etf',
            '4': 'derivative',
            '5': 'bond'
        }
        
        if choice not in type_map:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue
        
        instrument_type = type_map[choice]
        
        print(f"\nGenerating summary for {ticker} ({instrument_type})...")
        
        try:
            summary = generate_financial_summary(ticker, instrument_type)
            print("\n" + "="*80)
            print(f"SUMMARY FOR {ticker} ({instrument_type.upper()})")
            print("="*80)
            print(summary)
            print("="*80)
        except Exception as e:
            print(f"Error generating summary: {e}")

if __name__ == "__main__":
    main()

