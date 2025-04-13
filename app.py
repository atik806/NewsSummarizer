from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download required NLTK data
nltk.download('punkt')

class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.sources = {
            'bdnews24': {
                'url': 'https://bdnews24.com',
                'selectors': {
                    'articles': 'article, .article, .news-item',
                    'title': 'h3, h2, h1, .headline',
                    'link': 'a'
                }
            },
            'prothomalo': {
                'url': 'https://www.prothomalo.com',
                'selectors': {
                    'articles': 'article.story-card, div.story-card',
                    'title': 'h2.story-headline, h2.title',
                    'link': 'a'
                }
            },
            'jugantor': {
                'url': 'https://www.jugantor.com',
                'selectors': {
                    'articles': 'article, .news-item, .news-card',
                    'title': 'h2, h3, .headline',
                    'link': 'a'
                }
            },
            'ittefaq': {
                'url': 'https://www.ittefaq.com.bd',
                'selectors': {
                    'articles': 'article, .news-item, .news-card',
                    'title': 'h2, h3, .headline',
                    'link': 'a'
                }
            }
        }
    
    def get_news_from_source(self, source_name, limit=5):
        """Get news from a specific source"""
        if source_name not in self.sources:
            logging.error(f"Unknown source: {source_name}")
            return []
            
        source = self.sources[source_name]
        try:
            response = requests.get(source['url'], headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            
            # Try multiple selector patterns
            article_elements = soup.select(source['selectors']['articles'])
            
            if not article_elements:
                logging.info(f"No articles found with specific selectors for {source_name}, using fallback approach")
                for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                    link = heading.find_parent('a') or heading.find('a')
                    if link and link.get('href'):
                        title = heading.text.strip()
                        url = link.get('href')
                        
                        if not url.startswith('http'):
                            url = source['url'] + url
                            
                        articles.append({
                            'title': title,
                            'url': url,
                            'summary': self.get_article_summary(url),
                            'source': source_name
                        })
                        
                        if len(articles) >= limit:
                            break
            else:
                for article in article_elements[:limit]:
                    title_elem = article.select_one(source['selectors']['title'])
                    link_elem = article.select_one(source['selectors']['link'])
                    
                    if title_elem and link_elem:
                        title = title_elem.text.strip()
                        url = link_elem.get('href')
                        
                        if not url.startswith('http'):
                            url = source['url'] + url
                            
                        articles.append({
                            'title': title,
                            'url': url,
                            'summary': self.get_article_summary(url),
                            'source': source_name
                        })
            
            if not articles:
                logging.warning(f"Could not extract any headlines from {source_name}, using example data")
                articles = self.get_example_articles(source_name, limit)
            
            logging.info(f"Retrieved {len(articles)} headlines from {source_name}")
            return articles
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching headlines from {source_name}: {e}")
            return self.get_example_articles(source_name, limit)
    
    def get_example_articles(self, source_name, limit=5):
        """Get example articles for a specific source"""
        examples = {
            'bdnews24': [
                {'title': 'BDNews24: Bangladesh reports progress in economic growth', 
                 'url': 'https://bdnews24.com/',
                 'summary': 'Bangladesh has shown significant economic growth in recent years...',
                 'source': 'bdnews24'},
                {'title': 'BDNews24: New infrastructure projects announced in Dhaka', 
                 'url': 'https://bdnews24.com/',
                 'summary': 'Several new infrastructure projects have been announced for Dhaka...',
                 'source': 'bdnews24'}
            ],
            'prothomalo': [
                {'title': 'Prothom Alo: Education reforms to be implemented next year', 
                 'url': 'https://www.prothomalo.com/',
                 'summary': 'Major education reforms are planned for implementation next year...',
                 'source': 'prothomalo'},
                {'title': 'Prothom Alo: Health ministry launches new vaccination campaign', 
                 'url': 'https://www.prothomalo.com/',
                 'summary': 'The health ministry has launched a new vaccination campaign...',
                 'source': 'prothomalo'}
            ],
            'jugantor': [
                {'title': 'Jugantor: Tech industry in Bangladesh sees rapid growth', 
                 'url': 'https://www.jugantor.com/',
                 'summary': 'The technology industry in Bangladesh is experiencing rapid growth...',
                 'source': 'jugantor'},
                {'title': 'Jugantor: New agricultural initiatives announced', 
                 'url': 'https://www.jugantor.com/',
                 'summary': 'New agricultural initiatives have been announced to boost production...',
                 'source': 'jugantor'}
            ],
            'ittefaq': [
                {'title': 'Ittefaq: Cultural festival to be held next month', 
                 'url': 'https://www.ittefaq.com.bd/',
                 'summary': 'A major cultural festival is planned for next month...',
                 'source': 'ittefaq'},
                {'title': 'Ittefaq: Sports complex renovation completed', 
                 'url': 'https://www.ittefaq.com.bd/',
                 'summary': 'The renovation of the national sports complex has been completed...',
                 'source': 'ittefaq'}
            ]
        }
        return examples.get(source_name, [])[:limit]
    
    def get_article_summary(self, article_url):
        """Get a summary of the article content"""
        try:
            article = Article(article_url)
            article.download()
            article.parse()
            
            if article.text:
                parser = PlaintextParser.from_string(article.text, Tokenizer("english"))
                summarizer = LsaSummarizer()
                summary = summarizer(parser.document, 3)  # Get 3 sentences summary
                return ' '.join([str(sentence) for sentence in summary])
            else:
                return "Could not extract article content. The website structure may have changed or the content is not accessible."
            
        except Exception as e:
            logging.error(f"Error summarizing article: {e}")
            return "Click to read full article"

@app.route('/')
def home():
    scraper = NewsScraper()
    bdnews_articles = scraper.get_news_from_source('bdnews24', 5)
    prothomalo_articles = scraper.get_news_from_source('prothomalo', 5)
    jugantor_articles = scraper.get_news_from_source('jugantor', 5)
    ittefaq_articles = scraper.get_news_from_source('ittefaq', 5)
    
    return render_template('index.html', 
                         bdnews_articles=bdnews_articles,
                         prothomalo_articles=prothomalo_articles,
                         jugantor_articles=jugantor_articles,
                         ittefaq_articles=ittefaq_articles)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True) 