# 🤝 Alliyn - Business Networking Platform

A Tinder-like business networking platform that connects entrepreneurs and businesses for strategic partnerships, deals, and collaborations.

![Alliyn Business Networking](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/Frontend-React%2019-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen)

## 🚀 Features

### Core Business Matching
- **Tinder-style Swiping Interface** - Swipe through business profiles with intuitive gestures
- **Advanced Matching Algorithm** - 7-factor weighted scoring system including industry synergy, geographic compatibility, experience matching, and service area overlap
- **Business Profile Cards** - Rich profiles with company logos, descriptions, owner information, and partnership preferences

### Location-Based Filtering
- **Local Partnerships** - Find businesses within 20-mile radius using Haversine distance calculation
- **National Scope** - Connect with businesses nationwide
- **Geographic Compatibility** - Smart filtering based on service areas and business locations

### Premium Features
- **Free Tier** - 10 swipes and 1 match per day
- **Premium Upgrade** - Unlimited swipes, matches, and priority support for $19.99/month
- **Multiple Payment Options** - Credit Card, PayPal, and Apple Pay integration

### Monetization
- **3-Tier Sponsorship System**:
  - Basic Package: $500/month
  - Premium Package: $1,500/month  
  - Enterprise Package: Custom pricing
- **Industry-Based Quote Calculation** - Dynamic pricing based on industry multipliers
- **Popup Advertisement System** - Strategic ad placement for additional revenue

### Business Management
- **Profile Creation & Editing** - Comprehensive business profile management
- **Image Upload System** - Company logos and profile photos (base64 format)
- **Partnership Preferences** - Customizable partnership types and goals
- **Settings Management** - Persistent user preferences with localStorage

## 🛠 Tech Stack

### Frontend
- **React 19** - Modern React with hooks and functional components
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Axios** - HTTP client for API communication
- **React Router DOM** - Client-side routing

### Backend
- **FastAPI** - High-performance Python web framework
- **MongoDB** - NoSQL database with Motor async driver
- **Pydantic** - Data validation and serialization
- **CORS Middleware** - Cross-origin resource sharing support

### Development & Testing
- **Comprehensive Test Suite** - Backend API testing with 12+ test scenarios
- **Frontend Integration Tests** - Complete UI functionality verification
- **ESLint & Prettier** - Code quality and formatting
- **Hot Reload** - Development server with live reloading

## 📁 Project Structure

```
/app
├── backend/                 # FastAPI backend
│   ├── server.py           # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Backend environment variables
├── frontend/               # React frontend
│   ├── src/
│   │   └── App.js         # Main React application
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   └── .env              # Frontend environment variables
├── tests/                 # Test files
└── README.md             # Project documentation
```

## 🚦 Getting Started

### Prerequisites
- Node.js 16+ and Yarn
- Python 3.11+
- MongoDB
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd alliyn-business-networking
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
yarn install
```

4. **Environment Configuration**
Create `.env` files:

**Backend (.env)**:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=alliyn_business_network
```

**Frontend (.env)**:
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

5. **Start Services**
```bash
# Start MongoDB
sudo systemctl start mongodb

# Start Backend (Terminal 1)
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Start Frontend (Terminal 2)
cd frontend
yarn start
```

6. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/api

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest backend_test.py -v
```

### Frontend Testing
```bash
cd frontend
yarn test
```

## 🌟 Key Features Implemented

### ✅ Authentication System
- User signup and login
- Profile creation with immediate matching availability
- Session management

### ✅ Business Matching Engine
- Tinder-style swiping interface
- Advanced matching algorithm with industry synergy matrix
- Match history and management
- Geographic filtering (Local 20-mile radius vs National)

### ✅ Monetization System
- 3-tier sponsorship packages with quote generation
- Premium upgrade system with multiple payment options
- Strategic popup advertisement placement
- Industry-based pricing calculations

### ✅ Profile Management
- Comprehensive business profile creation
- Image upload system (logo and profile photos)
- Partnership preference configuration
- Real-time profile preview

### ✅ Location Intelligence
- Haversine distance calculation for local partnerships
- Coordinate system for major US cities
- Visual filtering indicators
- Remote business support

## 🔧 Configuration

### Environment Variables
- `MONGO_URL` - MongoDB connection string
- `DB_NAME` - Database name
- `REACT_APP_BACKEND_URL` - Backend API URL

### API Endpoints
All backend routes are prefixed with `/api`:
- `GET /api/` - Health check
- `POST/GET /api/status` - Status management
- `POST/GET /api/sponsorship` - Sponsorship system
- `GET /api/sponsorship/stats` - Sponsorship statistics

## 📈 Future Enhancements

- Integration with Airtable for admin backend
- AI-powered business matching recommendations
- Video profile introductions
- Advanced analytics dashboard
- Mobile app development
- Real-time messaging system

## 📄 License

This project is proprietary software developed for Alliyn Business Networking Platform.

## 🤝 Contributing

This is a private project. For access or collaboration inquiries, please contact the development team.

## 📞 Support

For technical support or business inquiries:
- Email: support@alliyn.com
- Platform: Emergent.sh deployment

---

**Built with ❤️ for connecting businesses and fostering strategic partnerships**