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
    # Craft prompts based on the financial instrument type
    prompts = {
        'stock': f"""
            You are a helpful financial advisor explaining concepts to beginners. 
            Please provide a beginner-friendly summary of stocks using a simple example of the stock with ticker {ticker}.
            Include information about:
            - What the company does
            - Why people might invest in this stock
            - Basic metrics beginners should know about (P/E ratio, dividend yield if applicable)
            - Potential risks to consider
            Keep explanations simple and avoid complex financial jargon.
        """,
        'index': f"""
            You are a helpful financial advisor explaining concepts to beginners.
            Please provide a beginner-friendly summary of indices and a simple example of an index that includes the company withsymbol {ticker}.
            Include information about:
            - What this index represents and tracks
            - Major components of this index
            - Why investors follow this index
            - How beginners might gain exposure to this index
            Keep explanations simple and avoid complex financial jargon.
        """,
        'etf': f"""
            You are a helpful financial advisor explaining concepts to beginners.
            Please provide a beginner-friendly summary of what ETFs are, using a simple example of a popular ETF that holds the company with symbol {ticker}
            Include information about:
            - What ETFs typically track or focus on
            - Major holdings or exposure
            - Fee structure (if you know it)
            - Why beginners might consider this ETF
            - Potential alternatives in the same category
            Keep explanations simple and avoid complex financial jargon.
        """,
        'derivative': f"""
            You are a helpful financial advisor explaining concepts to beginners.
            Please provide a beginner-friendly summary of derivatives.
            Include information about:
            - What a derivative is
            - The different types of assets that can be used as underlying assets for derivatives
            - Basic mechanics of derivatives work
            - Why investors might use derivatives
            - Potential risks for beginners
            - Use a simple example of a derivative with the company with symbol {ticker} as the underlying asset
            Keep explanations simple and avoid complex financial jargon.
        """,
        'bond': f"""
            You are a helpful financial advisor explaining concepts to beginners.
            Please provide a beginner-friendly summary of bonds.
            Include information about:
            - Why companies/governments/etc. issue bonds
            - An overview of the characteristics of bonds (term, yield, etc.)
            - The importance of credit quality/rating if applicable
            - Why investors might consider bonds
            - How interest rate changes can affect bonds 
            - Use a simple example of a bond with the company with symbol {ticker} as the issuer
            Keep explanations simple and avoid complex financial jargon.
        """
    }
    
    # Check if the instrument type is valid
    if instrument_type.lower() not in prompts:
        return f"Error: '{instrument_type}' is not a supported financial instrument type. Please choose from: stock, index, etf, derivative, or bond."
    
    # Get the appropriate prompt
    prompt = prompts[instrument_type.lower()]
    
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

