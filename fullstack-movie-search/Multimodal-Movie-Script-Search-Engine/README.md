# 🎬 Multimodal Movie Script Search Engine

A sophisticated AI-powered search engine that enables multimodal search across movie scripts, scenes, and dialogues using state-of-the-art machine learning models.

## 🎬 Features

- **Dialogue-to-Scene Search**: Find relevant movie scenes based on dialogue input
- **Scene-to-Dialogue Search**: Discover memorable dialogues from scene descriptions
- **Contextual Search**: Advanced search combining both dialogue and scene matching
- **Text Summarization**: AI-powered text summarization using BART
- **Script Generation**: Creative script generation using GPT-2
- **Real Movie Data**: Integration with TMDB and OMDB APIs for accurate movie information
- **Multimodal AI**: Combines CLIP, BERT, BART, and GPT-2 models
- **Modern UI/UX**: Clean, responsive interface with improved visibility

## 🚀 Tech Stack

### Backend (Modular Architecture)
- **Flask**: Web framework
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face transformers library
- **CLIP**: OpenAI's vision-language model
- **Sentence Transformers**: Text embeddings
- **BART**: Text summarization
- **GPT-2**: Text generation
- **Requests**: API integration

### Frontend
- **React**: UI framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Modern UI/UX**: Improved visibility with white backgrounds and clear text

## 📁 Project Structure

1. **Dialogue to Scene Search**
   - Enter movie dialogue in the text area
   - Click "Search for Scenes" 
   - View top-3 matching scenes with similarity scores

2. **Scene to Dialogue Search**
   - Upload a movie scene image
   - Click "Search for Dialogues"
   - View top-3 matching dialogues with context

3. **Contextual Search**
   - Enter dialogue text AND upload scene image
   - Click "Contextual Search"
   - View combined results with individual and combined similarity scores

### AI Tools

1. **Summarizer**
   - Paste movie script or dialogue text
   - Click "Generate Summary"
   - Get AI-powered concise summary with statistics

2. **Creative Generator**
   - Choose content type (Story/Poem/Dialogue)
   - Enter creative prompt
   - Generate AI-created content

## 📊 Sample Data

The application includes a dummy dataset with:
- **3 Movie Dialogues**: Matrix, Star Wars, Titanic
- **3 Scene Images**: Generated placeholder images with descriptions
- **Pre-computed Embeddings**: For fast search performance

### Sample Queries to Try:
- "There is no spoon"
- "May the Force be with you" 
- "I'm the king of the world"
- "You jump, I jump"

## 🏗️ Architecture

### Backend (Flask)
```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── README.md          # Backend documentation
```

### Frontend (React)
```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Main application pages
│   ├── services/      # API integration
│   ├── types/         # TypeScript type definitions
│   └── App.tsx        # Main application component
├── public/            # Static assets
├── package.json       # Node.js dependencies
└── tailwind.config.js # TailwindCSS configuration
```

## 🔧 Technical Details

### Model Loading
- Models are loaded at Flask startup for optimal performance
- Embeddings are pre-computed to avoid recomputation
- CORS enabled for cross-origin requests

### Performance Optimizations
- Caching of model outputs
- Efficient similarity computation using cosine similarity
- Lazy loading of heavy models
- Pre-computed embeddings for dataset

### Error Handling
- Comprehensive error handling in API endpoints
- User-friendly error messages in frontend
- Loading states and progress indicators

## 🚀 Future Enhancements

- [ ] Support for video clips and audio
- [ ] Integration with larger movie datasets (MSR-VTT, LSMDC)
- [ ] Advanced filtering and sorting options
- [ ] User authentication and favorites
- [ ] Batch processing capabilities
- [ ] Real-time collaboration features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for CLIP model
- Hugging Face for transformer models
- Sentence Transformers team
- React and TailwindCSS communities

## 🐛 Troubleshooting

### Common Issues

1. **Models taking too long to load**
   - First run downloads models (~2GB total)
   - Subsequent runs use cached models

2. **CORS errors**
   - Ensure Flask server is running on port 5000
   - Check API_BASE_URL in frontend configuration

3. **Memory issues**
   - Models require ~4GB RAM minimum
   - Consider using CPU-only mode for lower memory usage

### Support

For issues and questions, please open an issue on the GitHub repository.
