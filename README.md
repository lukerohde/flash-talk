# FlashSpeak

A Django-based language learning application that combines the power of spaced repetition with AI-powered voice interaction. Initially focused on Japanese language learning, with a vision to support multiple languages in the future.

## MVP Features & User Stories (Japanese)

We are migrating from our POC in /Users/lrohde/voice-anki to a proper django app in /Users/lrohde/voice-anki/app.

### Technical Architecture
- Server-side rendering with Django templates
- StimulusJS for interactive components
  - Flash Card Controller
  - Voice Chat Controller
  - Transcription Controller
- Asset bundling with NPM and Parcel
- Bootstrap 5 for responsive layout
- Uses OpenAI RealTime API for voice communication

### Voice Chat with AI Tutor
- As a language learner, I want to practice speaking Japanese with an AI tutor
  - DONE Bootstrap-based responsive layout with main content and sidebar
  - DONE Sliding sidebar on mobile, fixed on desktop (col-md-3)
  - DONE Main content area with transcript (col-md-9)
  - DONE Footer area for active flashcard review
  - DONE OpenAI session creation endpoint
  - DONE Stimulus voice controller with auto-connect

- As a learner, I want to see the conversation transcript in real-time
  - DONE Independent scrolling for transcript 
  - DONE Auto-scroll for new transcript entries
  - DONE Server-rendered transcript updates
  - The transcript knows if I'm speaking Japanese or English

- As a user, I want flexible microphone controls:
  - DONE WebRTC audio streaming setup
  - DONE Click to toggle mute/unmute
  - DONE Push-to-talk (walkie-talkie mode)
  - DONE Push-to-talk when not on hold disables the VAD temporarily for that response
  - UNTESTED Microphone input selection
  - DONE Disable Voice activity detection (VAD) when in walkie-talkie mode

### Flashcard Creation
- As a learner, I want to create flashcards directly from our conversation
  - DONE Ask AI to make flashcard (tool use)
  - Text selection handling in transcript
  - DONE Server-side flashcard creation endpoint
  - DONE Real-time sidebar update with new card
  - File upload
  - Make sure english is on the front
  - The AI can make multiple cards at a time
  - There is positive feedback when cards are made
  - Newly made cards go straight in for review

- As a learner, I want to create flashcards by selecting text from the transcript
  - Text selection event handling
  - Popup form for card creation
  - Card preview before saving

- As a learner, I want to review and edit flashcards
  - DONE List flashcards
  - DONE Delete flashcards
  - Search flashcards
  - Inline editing interface
  - Card update endpoint
  - Optimistic UI updates

- As a learner, I want to categorize my flashcards (multiple categories per card)
  - Category management in sidebar
  - Multi-select category interface
  - Category CRUD endpoints

### Flashcard Review
- As a learner, I want to review flashcards using spaced repetition (SM-2)
  - DONE Fetch next card
  - DONE AI reads card front and back
  - DONE Score card (Easy, Hard, Forgot)
  - DONE AI rates card (Easy, Hard, Forgot)
  - The user can override an AI judgement
  - The user can set the next review interval
  - The AI explains the users error succinctly, instead of just moving straight to the next card
  - DONE SM-2 algorithm implementation
  - DONE Review scheduling system
  - DONE Review state persistence

- As a learner, I want the app to work nicely on mobile
  - DONE Responsive layout with sidebar and main content
  - DONE Auto-scroll for new transcript entries
  - DONE Sidebar collapses
  - Mute/Unmute button at easy reach
  - Self assessment buttons at easy reach - perhaps swipe

- As a learner, I want to practice pronunciation and discuss cards during reviews
  - DONE Integration with voice chat system
  - DONE Card-specific conversation context
  - Progress tracking during review
  - The AI is careful about pronounciation

- As a learner, I want to filter reviews by category
  - Category filter interface in sidebar
  - DONE Dynamic review queue updates
  - Review statistics by category

- As a learner, I want to track my review progress
  - Review history tracking
  - Progress visualization
  - Statistics calculation endpoints

## Future Features

### Multi-language Support
- As a language learner, I want to practice my language of choice
- As a language learner, I want to configure AI tutor prompts for my specific learning needs
- As a language learner, I want to reset tutor prompts to default settings
- As a language learner, I want to customize the tutor's teaching style and focus areas


## Setup

Run the setup script to configure your project name and `.env` plus `docker-compose.override.yml` for local development.

```
./setup
```

This will setup your .env and docker-compose.override.yml file for local development.

```
docker-compose up -d
```

see logs
```
docker-compose logs
```

Shell into the python app container
```
docker-compose exec app /bin/bash
```

To make typing these commands less tedious it helps to have docker aliases in your .bash_profile or similar
```
alias dc='docker-compose'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs'
```

Once in the app container you can run the django commands
```
python manage.py runserver 0.0.0.0:3000
``` 

To rebuild your javascript
```
npm run build
```

To have up to date not reloading CSS and JS during development
```
npm run dev
``` 

To run with a production gunicorn server
```
./start
```

To run tests
```
pytest
```

To run playwright tests in headed mode
Start your x server (hint: `brew install xquartz` and permit your server)

```
pytest --headed
```

To debug your playwright tests
```
PWDEBUG=1 pytest --headed
```

To view and debug your app on mobile (mobile webrtc needs https) or share a dev preview external 

```brew install ngrok```

Sign up and setup your token [here](https://dashboard.ngrok.com/get-started/your-authtoken)
```
ngrok http 3000
```

Responsive design mode for 
- ios mini 13: 375 x 812

# Deployment Instructions

For more detailed instructions, please refer to the following README files:

- [Deploy to AWS](deploy-aws-infra/pulumi/README.md) - just the asset bucket
- [Deploy to Render](deploy-render/README.md)
- [Deploy to Digital Ocean](deploy-do/README.md)