# NewsSummarizer

A web application that provides AI-powered news summaries from leading Bangladeshi newspapers. Stay informed with concise, accurate summaries of the latest news.

## Features

- **Real-time News Aggregation**: Fetches news from multiple Bangladeshi newspapers
- **AI-Powered Summaries**: Generates concise summaries of news articles
- **Multiple Sources**: Currently supports:
  - BDNews24
  - Prothom Alo
  - Jugantor
  - Ittefaq
- **User-Friendly Interface**: Clean, modern design with responsive layout
- **Dark Mode Support**: Switch between light and dark themes
- **Share Functionality**: Share articles with others

## Technologies Used

- **Backend**:
  - Python Flask
  - BeautifulSoup for web scraping
  - Newspaper3k for article extraction
  - Sumy for text summarization

- **Frontend**:
  - HTML5
  - CSS3 with CSS Variables
  - JavaScript
  - Font Awesome icons

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NewsSummarizer.git
cd NewsSummarizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
NewsSummarizer/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Stylesheets
│   └── js/
│       └── main.js    # JavaScript files
├── templates/
│   ├── index.html     # Home page
│   └── about.html     # About page
└── README.md          # Project documentation
```

## Features in Detail

### News Aggregation
- Real-time fetching of news articles
- Support for multiple news sources
- Automatic article extraction and processing

### Summarization
- AI-powered text summarization
- Preserves key information
- Maintains context and readability

### User Interface
- Responsive design for all devices
- Dark mode support
- Clean and intuitive navigation
- Share functionality for articles

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Font Awesome for icons
- Flask community for the web framework
- All news sources for their content

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/NewsSummarizer](https://github.com/yourusername/NewsSummarizer) 