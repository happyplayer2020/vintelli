from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os
import json
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Mock product database with sold items for comparison
MOCK_SOLD_ITEMS = [
    {
        "title": "Nike Air Max 90 Sneakers",
        "brand": "Nike",
        "category": "Shoes",
        "original_price": 45,
        "sold_price": 85,
        "days_to_sell": 3,
        "condition": "Used - Good",
        "size": "42"
    },
    {
        "title": "Levi's 501 Original Jeans",
        "brand": "Levi's",
        "category": "Jeans",
        "original_price": 25,
        "sold_price": 55,
        "days_to_sell": 7,
        "condition": "Used - Good",
        "size": "32/32"
    },
    {
        "title": "Zara Blazer Jacket",
        "brand": "Zara",
        "category": "Blazers",
        "original_price": 35,
        "sold_price": 65,
        "days_to_sell": 12,
        "condition": "Used - Very Good",
        "size": "M"
    },
    {
        "title": "Adidas Ultraboost Running Shoes",
        "brand": "Adidas",
        "category": "Shoes",
        "original_price": 60,
        "sold_price": 120,
        "days_to_sell": 5,
        "condition": "Used - Excellent",
        "size": "41"
    },
    {
        "title": "H&M Summer Dress",
        "brand": "H&M",
        "category": "Dresses",
        "original_price": 15,
        "sold_price": 28,
        "days_to_sell": 15,
        "condition": "Used - Good",
        "size": "S"
    },
    {
        "title": "Uniqlo Cashmere Sweater",
        "brand": "Uniqlo",
        "category": "Sweaters",
        "original_price": 20,
        "sold_price": 45,
        "days_to_sell": 8,
        "condition": "Used - Very Good",
        "size": "L"
    },
    {
        "title": "Converse Chuck Taylor All Star",
        "brand": "Converse",
        "category": "Shoes",
        "original_price": 30,
        "sold_price": 55,
        "days_to_sell": 4,
        "condition": "Used - Good",
        "size": "39"
    },
    {
        "title": "Mango Leather Bag",
        "brand": "Mango",
        "category": "Bags",
        "original_price": 40,
        "sold_price": 75,
        "days_to_sell": 10,
        "condition": "Used - Very Good",
        "size": "One Size"
    },
    {
        "title": "Pull&Bear Denim Jacket",
        "brand": "Pull&Bear",
        "category": "Jackets",
        "original_price": 25,
        "sold_price": 48,
        "days_to_sell": 6,
        "condition": "Used - Good",
        "size": "M"
    },
    {
        "title": "Bershka Crop Top",
        "brand": "Bershka",
        "category": "Tops",
        "original_price": 8,
        "sold_price": 18,
        "days_to_sell": 20,
        "condition": "Used - Good",
        "size": "S"
    },
    {
        "title": "Ralph Lauren Polo Shirt",
        "brand": "Ralph Lauren",
        "category": "Shirts",
        "original_price": 25,
        "sold_price": 45,
        "days_to_sell": 5,
        "condition": "Used - Very Good",
        "size": "M"
    },
    {
        "title": "Ralph Lauren Chino Pants",
        "brand": "Ralph Lauren",
        "category": "Pants",
        "original_price": 30,
        "sold_price": 55,
        "days_to_sell": 8,
        "condition": "Used - Good",
        "size": "32/32"
    },
    {
        "title": "Ralph Lauren Sweater",
        "brand": "Ralph Lauren",
        "category": "Sweaters",
        "original_price": 35,
        "sold_price": 65,
        "days_to_sell": 6,
        "condition": "Used - Excellent",
        "size": "L"
    }
]

def scrape_vinted_item(url):
    """Scrape product information from Vinted item page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }
        
        # Try with session for better handling
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product information with more comprehensive selectors
        title = ""
        price = ""
        brand = ""
        size = ""
        category = ""
        condition = ""
        
        # Try multiple selectors for title
        title_selectors = [
            'h1[data-testid="item-title"]',
            'h1',
            '[data-testid="item-title"]',
            '.item-title',
            'title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                if title and title != "Vinted":
                    break
        
        # Try multiple selectors for price - Vinted specific
        price_selectors = [
            '[data-testid="item-price"]',
            '[data-testid="price"]',
            '.web_ui__Text__text',
            '[class*="price"]',
            '[class*="Price"]',
            'span[class*="price"]',
            'div[class*="price"]',
            '[class*="amount"]',
            '[class*="Amount"]',
            'span[class*="amount"]',
            'div[class*="amount"]',
            '[data-testid*="price"]',
            '[data-testid*="Price"]',
            '[class*="cost"]',
            '[class*="Cost"]',
            # Vinted specific selectors
            '[data-testid="item-price"] span',
            '[data-testid="price"] span',
            '.web_ui__Text__text[class*="price"]',
            '.web_ui__Text__text[class*="Price"]',
            # Look for any element containing price-like text
            'span:contains("€")',
            'div:contains("€")',
            'p:contains("€")'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text().strip()
                print(f"Found price element with text: {price_text}")  # Debug
                
                # Look for various price formats
                price_patterns = [
                    r'€(\d+(?:[.,]\d+)?)',
                    r'(\d+(?:[.,]\d+)?)\s*€',
                    r'(\d+(?:[.,]\d+)?)',
                    r'(\d+)\s*EUR',
                    r'(\d+)\s*euro'
                ]
                for pattern in price_patterns:
                    price_match = re.search(pattern, price_text)
                    if price_match:
                        price = price_match.group(1).replace(',', '.')
                        print(f"Extracted price: {price}")  # Debug
                        break
                if price:
                    break
        
        # If still no price, try to find any number that looks like a price
        if not price:
            # Look for any text containing numbers and euro symbols
            all_text = soup.get_text()
            price_matches = re.findall(r'€\s*(\d+(?:[.,]\d+)?)', all_text)
            if price_matches:
                price = price_matches[0].replace(',', '.')
                print(f"Found price in page text: {price}")  # Debug
        
        # Debug: Print the entire HTML to see what we're working with
        if not price:
            print("DEBUG: No price found, printing page structure...")
            print("Page title:", soup.title.get_text() if soup.title else "No title")
            print("All text containing '€':")
            all_text = soup.get_text()
            euro_lines = [line.strip() for line in all_text.split('\n') if '€' in line]
            for line in euro_lines[:10]:  # Show first 10 lines with euro
                print(f"  {line}")
            
            # Try to find any number that could be a price (between 5 and 500 euros)
            all_numbers = re.findall(r'(\d{1,3}(?:[.,]\d{2})?)', all_text)
            potential_prices = [num for num in all_numbers if 5 <= float(num.replace(',', '.')) <= 500]
            if potential_prices:
                # Take the first reasonable price found
                price = potential_prices[0].replace(',', '.')
                print(f"Found potential price from numbers: {price}")
        
        # Try multiple selectors for brand
        brand_selectors = [
            'a[href*="/brand/"]',
            '[data-testid="item-brand"]',
            '.brand',
            '.item-brand',
            'a[href*="brand"]'
        ]
        
        for selector in brand_selectors:
            brand_elem = soup.select_one(selector)
            if brand_elem:
                brand = brand_elem.get_text().strip()
                if brand and brand.lower() not in ['brand', 'marque']:
                    break
        
        # Try multiple selectors for size
        size_selectors = [
            '[data-testid="item-size"]',
            '.size',
            '.item-size',
            'span:contains("Size")',
            'span:contains("Taille")'
        ]
        
        for selector in size_selectors:
            size_elem = soup.select_one(selector)
            if size_elem:
                size_text = size_elem.get_text().strip()
                if 'size' in size_text.lower() or 'taille' in size_text.lower():
                    # Extract just the size value
                    size_match = re.search(r'(?:Size|Taille)[:\s]*([^\s]+)', size_text, re.IGNORECASE)
                    if size_match:
                        size = size_match.group(1)
                    else:
                        size = size_text
                    break
        
        # Try multiple selectors for category
        category_selectors = [
            'a[href*="/catalog/"]',
            '[data-testid="item-category"]',
            '.category',
            '.item-category',
            'nav a[href*="catalog"]'
        ]
        
        for selector in category_selectors:
            category_elem = soup.select_one(selector)
            if category_elem:
                category = category_elem.get_text().strip()
                if category and category.lower() not in ['catalog', 'catégorie']:
                    break
        
        # Try multiple selectors for condition
        condition_selectors = [
            '[data-testid="item-condition"]',
            '.condition',
            '.item-condition',
            'span:contains("Condition")',
            'span:contains("État")'
        ]
        
        for selector in condition_selectors:
            condition_elem = soup.select_one(selector)
            if condition_elem:
                condition_text = condition_elem.get_text().strip()
                if 'condition' in condition_text.lower() or 'état' in condition_text.lower():
                    # Extract just the condition value
                    condition_match = re.search(r'(?:Condition|État)[:\s]*(.+)', condition_text, re.IGNORECASE)
                    if condition_match:
                        condition = condition_match.group(1).strip()
                    else:
                        condition = condition_text
                    break
        
        # Fallback: try to extract from breadcrumbs or navigation
        if not category:
            breadcrumbs = soup.find_all('a', href=re.compile(r'/catalog/'))
            if breadcrumbs:
                category = breadcrumbs[-1].get_text().strip()
        
        if not brand:
            # Try to extract brand from title
            if title:
                brand_match = re.search(r'(\w+)\s+(?:Pantalon|Pants|Shirt|T-shirt|Sweater|Jacket|Shoes|Sneakers)', title, re.IGNORECASE)
                if brand_match:
                    brand = brand_match.group(1)
        
        return {
            'title': title,
            'price': price,
            'brand': brand,
            'size': size,
            'category': category,
            'condition': condition,
            'url': url
        }
        
    except Exception as e:
        print(f"Error scraping Vinted item: {e}")
        return None

def create_fallback_data(url):
    """Create fallback data when scraping fails"""
    try:
        # Extract item ID from URL
        item_id_match = re.search(r'/items/(\d+)', url)
        if not item_id_match:
            return None
        
        # Extract basic info from URL path
        url_parts = url.split('/')
        title_part = url_parts[-1] if len(url_parts) > 1 else ''
        
        # Clean up title
        title = title_part.replace('-', ' ').title()
        if title.endswith('.html'):
            title = title[:-5]
        
        # Try to extract brand from title
        brand = ""
        if 'ralph' in title.lower() and 'lauren' in title.lower():
            brand = "Ralph Lauren"
        elif 'nike' in title.lower():
            brand = "Nike"
        elif 'adidas' in title.lower():
            brand = "Adidas"
        elif 'levi' in title.lower():
            brand = "Levi's"
        elif 'zara' in title.lower():
            brand = "Zara"
        elif 'h&m' in title.lower() or 'hm' in title.lower():
            brand = "H&M"
        
        # Determine category from title
        category = "Clothing"
        if any(word in title.lower() for word in ['pantalon', 'pants', 'jeans', 'trousers']):
            category = "Pants"
        elif any(word in title.lower() for word in ['shirt', 't-shirt', 'polo']):
            category = "Shirts"
        elif any(word in title.lower() for word in ['sweater', 'pull', 'hoodie']):
            category = "Sweaters"
        elif any(word in title.lower() for word in ['jacket', 'blazer', 'veste']):
            category = "Jackets"
        elif any(word in title.lower() for word in ['shoes', 'sneakers', 'chaussures']):
            category = "Shoes"
        elif any(word in title.lower() for word in ['dress', 'robe']):
            category = "Dresses"
        
        # Try to estimate a realistic price based on brand and category
        estimated_price = '25.00'  # Default
        if brand == "Ralph Lauren":
            if category == "Pants":
                estimated_price = '35.00'
            elif category == "Shirts":
                estimated_price = '30.00'
            elif category == "Sweaters":
                estimated_price = '40.00'
        elif brand == "Nike":
            estimated_price = '45.00'
        elif brand == "Adidas":
            estimated_price = '40.00'
        elif brand == "Levi's":
            estimated_price = '30.00'
        elif brand == "Zara":
            estimated_price = '20.00'
        elif brand == "H&M":
            estimated_price = '15.00'
        
        return {
            'title': title,
            'price': estimated_price,
            'brand': brand,
            'size': 'M',  # Default size
            'category': category,
            'condition': 'Used - Good',  # Default condition
            'url': url,
            'fallback': True  # Mark as fallback data
        }
        
    except Exception as e:
        print(f"Error creating fallback data: {e}")
        return None

def analyze_resell_potential(item_data, comparison_data):
    """Analyze resell potential using OpenAI GPT-4 with much better prompts"""
    try:
        # Calculate fees and shipping estimates
        original_price = float(item_data.get('price', 0))
        shipping_cost = 5.0  # Estimated shipping cost
        platform_fees = original_price * 0.05  # 5% platform fees
        total_cost = original_price + shipping_cost + platform_fees
        
        # Prepare a much more detailed and specific prompt
        prompt = f"""
You are an expert Vinted reseller with 5+ years of experience. Analyze this item for reselling potential.

ITEM TO ANALYZE:
- Title: {item_data.get('title', 'N/A')}
- Current Price: €{item_data.get('price', 'N/A')}
- Brand: {item_data.get('brand', 'N/A')}
- Size: {item_data.get('size', 'N/A')}
- Category: {item_data.get('category', 'N/A')}
- Condition: {item_data.get('condition', 'N/A')}

SIMILAR SOLD ITEMS (for reference):
{json.dumps(comparison_data, indent=2)}

ANALYSIS REQUIREMENTS:
1. Resellability: Consider brand popularity, demand, seasonality, and competition
2. Resale Price: Base on similar sold items, brand value, and current market
3. Time to Sell: Consider demand, season, and competition level
4. Profit Calculation: Resale price - original price - €5 shipping - 5% platform fees
5. Risks: Market saturation, seasonal factors, condition issues, etc.

Provide your analysis in this EXACT JSON format:
{{
    "resellable": "Yes" or "No",
    "estimated_resale_price": "€XX.XX",
    "time_to_sell": "X-X days",
    "estimated_profit": "€XX.XX",
    "risks": "Specific risk factors"
}}

IMPORTANT: Be realistic and conservative. Consider that:
- Vinted has high competition
- Shipping costs €5
- Platform fees are 5%
- Most items take 7-30 days to sell
- Profit margins are typically 20-50% for good items
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional Vinted reseller. Provide realistic, data-driven analysis. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.2
        )
        
        # Parse the response
        analysis_text = response.choices[0].message.content.strip()
        print(f"OpenAI Response: {analysis_text}")  # Debug
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                
                # Validate and clean the analysis
                if not analysis.get('resellable'):
                    analysis['resellable'] = 'No'
                if not analysis.get('estimated_resale_price'):
                    analysis['estimated_resale_price'] = f"€{original_price + 10:.2f}"
                if not analysis.get('time_to_sell'):
                    analysis['time_to_sell'] = '7-14 days'
                if not analysis.get('estimated_profit'):
                    # Calculate a reasonable profit
                    resale_price = float(analysis.get('estimated_resale_price', '€50').replace('€', ''))
                    profit = resale_price - total_cost
                    analysis['estimated_profit'] = f"€{max(0, profit):.2f}"
                if not analysis.get('risks'):
                    analysis['risks'] = 'Market analysis needed'
                    
            else:
                # If no JSON found, create a smart fallback based on data
                analysis = create_smart_fallback_analysis(item_data, comparison_data, original_price, total_cost)
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Create smart fallback analysis
            analysis = create_smart_fallback_analysis(item_data, comparison_data, original_price, total_cost)
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing with OpenAI: {e}")
        # Create smart fallback analysis
        return create_smart_fallback_analysis(item_data, comparison_data, float(item_data.get('price', 0)), 0)

def create_smart_fallback_analysis(item_data, comparison_data, original_price, total_cost):
    """Create intelligent fallback analysis when OpenAI fails"""
    brand = item_data.get('brand', '').lower()
    category = item_data.get('category', '').lower()
    
    # Brand-based analysis
    brand_multipliers = {
        'ralph lauren': 1.8,
        'nike': 1.6,
        'adidas': 1.5,
        "levi's": 1.4,
        'zara': 1.3,
        'h&m': 1.2,
        'uniqlo': 1.4,
        'mango': 1.3,
        'bershka': 1.2,
        'pull&bear': 1.2
    }
    
    # Get multiplier for this brand
    multiplier = 1.3  # Default
    for brand_name, brand_mult in brand_multipliers.items():
        if brand_name in brand:
            multiplier = brand_mult
            break
    
    # Calculate estimated resale price
    estimated_resale = original_price * multiplier
    
    # Adjust based on category
    if 'shoes' in category or 'sneakers' in category:
        estimated_resale *= 1.1  # Shoes sell well
    elif 'jeans' in category:
        estimated_resale *= 1.05  # Jeans are reliable
    elif 'dresses' in category:
        estimated_resale *= 0.9  # Dresses can be seasonal
    
    # Calculate profit
    profit = estimated_resale - total_cost
    
    # Determine resellability
    resellable = "Yes" if profit > 5 and multiplier > 1.2 else "No"
    
    # Time to sell based on brand popularity
    if multiplier > 1.5:
        time_to_sell = "3-7 days"
    elif multiplier > 1.3:
        time_to_sell = "7-14 days"
    else:
        time_to_sell = "14-30 days"
    
    # Risk assessment
    risks = []
    if multiplier < 1.3:
        risks.append("Low brand recognition")
    if 'dresses' in category:
        risks.append("Seasonal demand")
    if profit < 10:
        risks.append("Low profit margin")
    if not risks:
        risks.append("Standard market risks")
    
    return {
        "resellable": resellable,
        "estimated_resale_price": f"€{estimated_resale:.2f}",
        "time_to_sell": time_to_sell,
        "estimated_profit": f"€{max(0, profit):.2f}",
        "risks": ", ".join(risks)
    }

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a Vinted item for resell potential"""
    try:
        data = request.get_json()
        vinted_url = data.get('url', '').strip()
        
        if not vinted_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        if 'www.vinted' not in vinted_url:
            return jsonify({'error': 'Please provide a valid Vinted URL'}), 400
        
        # Scrape the Vinted item
        item_data = scrape_vinted_item(vinted_url)
        
        # If scraping fails, create fallback data from URL
        if not item_data:
            # Extract basic info from URL as fallback
            fallback_data = create_fallback_data(vinted_url)
            if fallback_data:
                item_data = fallback_data
            else:
                return jsonify({'error': 'Failed to scrape item data'}), 500
        
        # Find similar items for comparison
        similar_items = []
        
        # First try to find items with the same brand
        if item_data.get('brand'):
            brand_similar = [
                item for item in MOCK_SOLD_ITEMS 
                if item['brand'].lower() == item_data['brand'].lower()
            ]
            similar_items.extend(brand_similar)
        
        # Then try to find items with the same category
        if item_data.get('category'):
            category_similar = [
                item for item in MOCK_SOLD_ITEMS 
                if item['category'].lower() == item_data['category'].lower() and 
                item not in similar_items
            ]
            similar_items.extend(category_similar)
        
        # If still no similar items, try partial brand matches
        if not similar_items and item_data.get('brand'):
            partial_brand_similar = [
                item for item in MOCK_SOLD_ITEMS 
                if item_data['brand'].lower() in item['brand'].lower() or 
                item['brand'].lower() in item_data['brand'].lower()
            ]
            similar_items.extend(partial_brand_similar)
        
        # If still no similar items, try category keywords
        if not similar_items and item_data.get('category'):
            category_keywords = {
                'hommes': ['jeans', 'pants', 'trousers', 'shirts', 'tops'],
                'femmes': ['dresses', 'tops', 'skirts', 'blouses'],
                'chaussures': ['shoes', 'sneakers', 'boots'],
                'sacs': ['bags', 'handbags', 'backpacks'],
                'accessoires': ['accessories', 'jewelry', 'watches']
            }
            
            current_category = item_data['category'].lower()
            for keyword, related_categories in category_keywords.items():
                if keyword in current_category or any(cat in current_category for cat in related_categories):
                    keyword_similar = [
                        item for item in MOCK_SOLD_ITEMS 
                        if any(cat in item['category'].lower() for cat in related_categories)
                    ]
                    similar_items.extend(keyword_similar)
                    break
        
        # If no similar items found, use items with similar price range
        if not similar_items and item_data.get('price'):
            try:
                item_price = float(item_data['price'])
                price_range_similar = [
                    item for item in MOCK_SOLD_ITEMS 
                    if abs(item['original_price'] - item_price) <= 20  # Within €20 range
                ]
                similar_items.extend(price_range_similar)
            except (ValueError, TypeError):
                pass
        
        # If still no similar items, use a mix of popular items
        if not similar_items:
            # Get items that are likely to be similar based on common categories
            popular_categories = ['Shoes', 'Jeans', 'Sweaters', 'Jackets']
            similar_items = [
                item for item in MOCK_SOLD_ITEMS 
                if item['category'] in popular_categories
            ][:3]
        
        # Ensure we don't have duplicates and limit to top 3
        unique_similar_items = []
        seen = set()
        for item in similar_items:
            item_key = f"{item['brand']}-{item['title']}"
            if item_key not in seen:
                unique_similar_items.append(item)
                seen.add(item_key)
            if len(unique_similar_items) >= 3:
                break
        
        similar_items = unique_similar_items
        
        # Analyze resell potential
        analysis = analyze_resell_potential(item_data, similar_items)
        
        # Prepare response
        response_data = {
            'item_data': item_data,
            'analysis': analysis,
            'similar_items': similar_items[:3]  # Show top 3 similar items
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 