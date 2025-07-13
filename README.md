# Vintelli - AI-Powered Vinted Resell Value Analyzer

Vintelli is a full-stack micro-SaaS web application that helps Vinted resellers evaluate whether an item they want to buy is good for reselling. The app uses AI to analyze product data and provide insights on profitability, time to sell, and potential risks.

## Features

- **Smart Product Analysis**: Scrapes Vinted product pages to extract key information
- **AI-Powered Insights**: Uses OpenAI GPT-4 to analyze resell potential
- **Profitability Scoring**: Provides estimated profit, resale price, and time to sell
- **Risk Assessment**: Identifies potential downsides and market risks
- **Similar Item Comparison**: Shows recently sold similar items for reference
- **Mobile-Friendly Design**: Clean, modern UI that works on all devices

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **AI**: OpenAI GPT-4 API
- **Web Scraping**: BeautifulSoup4
- **Styling**: Custom CSS with responsive design

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vintelli
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```
   
   Get your OpenAI API key from: https://platform.openai.com/api-keys

5. **Run the application**
   ```bash
   # Option 1: Use the startup script (recommended)
   python run.py
   
   # Option 2: Run directly
   python app.py
   ```

6. **Test the setup (optional)**
   ```bash
   python test_setup.py
   ```

7. **Open your browser**
   
   Navigate to `http://localhost:5000`

## Usage

1. **Paste a Vinted URL**: Copy a product URL from Vinted and paste it into the input field
2. **Click "Check Resell Value"**: The app will analyze the item and provide insights
3. **Review Results**: See the analysis including:
   - ✅ Resellability (Yes/No)
   - 💸 Potential Profit
   - 🕒 Time to Flip
   - 💡 Recommended Resell Price
   - ⚠️ Risk Summary
4. **Compare with Similar Items**: View recently sold similar items for reference

## Project Structure

```
vintelli/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # CSS styles
    └── script.js         # JavaScript functionality
```

## API Endpoints

- `GET /` - Main application page
- `POST /analyze` - Analyze a Vinted item for resell potential

### Analyze Endpoint

**Request:**
```json
{
  "url": "https://www.vinted.com/items/..."
}
```

**Response:**
```json
{
  "item_data": {
    "title": "Product Title",
    "price": "25.00",
    "brand": "Brand Name",
    "size": "M",
    "category": "Category",
    "condition": "Used - Good"
  },
  "analysis": {
    "resellable": "Yes",
    "estimated_resale_price": "€45",
    "time_to_sell": "7-14 days",
    "estimated_profit": "€15",
    "risks": "Market is competitive"
  },
  "similar_items": [...]
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable debug mode (True/False)

### Customization

You can customize the mock database by modifying the `MOCK_SOLD_ITEMS` list in `app.py`. This contains example sold items used for comparison analysis.

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

For production deployment, consider using:

1. **WSGI Server**: Gunicorn or uWSGI
2. **Reverse Proxy**: Nginx
3. **Process Manager**: PM2 or Supervisor
4. **Environment**: Set `FLASK_ENV=production`

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Limitations

- **Web Scraping**: Vinted may change their HTML structure, requiring updates to the scraping logic
- **API Rate Limits**: OpenAI API has rate limits that may affect high-volume usage
- **Data Accuracy**: Analysis is based on mock data and AI predictions, not real-time market data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue on GitHub.

---

**Note**: This is an MVP (Minimum Viable Product) version. For production use, consider adding:
- User authentication
- Database for storing analysis history
- Real-time market data integration
- Payment processing
- Advanced analytics and reporting 