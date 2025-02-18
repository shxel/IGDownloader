```markdown
# IGDownloader 📥  
**Download Instagram Content Effortlessly**

A Python-based tool to download Instagram posts, stories, highlights, and IGTV content in various formats and resolutions.

## Features ✨
- Download public/private Instagram posts (images, videos, and carousels)
- Save stories and highlights from public accounts
- Fetch IGTV videos with metadata
- Multiple quality/resolution options
- Command-line interface for easy integration
- Batch download capabilities

## Installation 🛠️

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/shxel/IGDownloader.git
   cd IGDownloader
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🚀

### Basic Command
```bash
python IGDownloader.py [options]
```

### Examples
**Download a post:**
```bash
python IGDownloader.py --url https://www.instagram.com/p/CxamplePost/ --type post --output ./downloads
```

**Save user stories:**
```bash
python IGDownloader.py --user username --type story --quality high
```

**Download IGTV video:**
```bash
python IGDownloader.py --url https://www.instagram.com/tv/CxampleIGTV/ --type igtv
```

### Options
```
--url         Instagram content URL
--user        Target Instagram username
--type        Content type (post, story, highlight, igtv)
--output      Output directory (default: ./downloads)
--quality     Video quality (low, medium, high)
--batch       Batch mode (reads URLs from urls.txt)
--metadata    Save metadata (caption, timestamp, likes)
```

## Configuration ⚙️
Create `.env` file for credentials (required for private accounts):
```ini
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

**Note:** Never commit your credentials! Add `.env` to `.gitignore`

## Contributing 🤝
We welcome contributions! Please follow these steps:
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please discuss major changes via Issues first.

## License 📄
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚠️
This project is for educational purposes only. Respect Instagram's Terms of Service and only download content you have rights to access. Developers are not responsible for misuse of this tool.

---
**Happy Downloading!** 🎉  
If you find this useful, please consider ⭐ starring the repository!
``` 
