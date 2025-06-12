import React, { useState, useRef, useCallback } from 'react';
import './App.css';

// Mock business data with comprehensive profiles
const mockBusinesses = [
  {
    id: 1,
    companyName: "TechFlow Solutions",
    companyDescription: "AI-powered business automation platform helping companies streamline operations",
    logo: "https://images.unsplash.com/photo-1663124178667-28b3776d7c15",
    ownerName: "Sarah Chen",
    ownerTitle: "CEO & Founder",
    profileImage: "https://images.pexels.com/photos/19245168/pexels-photo-19245168.jpeg",
    serviceAreas: ["San Francisco", "Silicon Valley", "Remote"],
    industry: "Technology",
    yearsInBusiness: 3,
    seekingPartnership: "National",
    partnerships: ["Strategic Alliances", "Joint Ventures", "Co-Branding"]
  },
  {
    id: 2,
    companyName: "Green Energy Consulting",
    companyDescription: "Sustainable energy solutions for businesses looking to reduce carbon footprint",
    logo: "https://images.unsplash.com/photo-1693801873650-b1091c25abbf",
    ownerName: "Michael Rodriguez",
    ownerTitle: "Managing Director",
    profileImage: "https://images.unsplash.com/photo-1576558656222-ba66febe3dec",
    serviceAreas: ["Los Angeles", "Orange County", "San Diego"],
    industry: "Renewable Energy",
    yearsInBusiness: 8,
    seekingPartnership: "Local",
    partnerships: ["Affiliate Partnerships", "Event Collaborations", "Sponsorship Agreements"]
  },
  {
    id: 3,
    companyName: "Digital Marketing Pro",
    companyDescription: "Full-service digital marketing agency specializing in growth hacking for startups",
    logo: "https://images.unsplash.com/photo-1740587010576-0ecff8049c8f",
    ownerName: "Jessica Thompson",
    ownerTitle: "Creative Director",
    profileImage: "https://images.unsplash.com/photo-1590496552566-41aca09db352",
    serviceAreas: ["New York", "Boston", "Philadelphia"],
    industry: "Marketing & Advertising",
    yearsInBusiness: 5,
    seekingPartnership: "National",
    partnerships: ["Co-Branding", "Joint Ventures", "Event Collaborations"]
  },
  {
    id: 4,
    companyName: "FinTech Innovations",
    companyDescription: "Revolutionary financial technology solutions for modern businesses",
    logo: "https://images.unsplash.com/photo-1637844528486-6dc108bd5c7f",
    ownerName: "David Park",
    ownerTitle: "CEO",
    profileImage: "https://images.unsplash.com/photo-1507679799987-c73779587ccf",
    serviceAreas: ["Chicago", "Milwaukee", "Madison"],
    industry: "Financial Technology",
    yearsInBusiness: 4,
    seekingPartnership: "National",
    partnerships: ["Strategic Alliances", "Incubator/Accelerator Collaborations"]
  },
  {
    id: 5,
    companyName: "Wellness Hub Co.",
    companyDescription: "Corporate wellness programs designed to boost employee productivity and happiness",
    logo: "https://images.unsplash.com/photo-1617091076336-03dc99aff1df",
    ownerName: "Amanda Foster",
    ownerTitle: "Founder & Wellness Expert",
    profileImage: "https://images.unsplash.com/photo-1425421669292-0c3da3b8f529",
    serviceAreas: ["Miami", "Tampa", "Orlando"],
    industry: "Health & Wellness",
    yearsInBusiness: 2,
    seekingPartnership: "Local",
    partnerships: ["Affiliate Partnerships", "Sponsorship Agreements", "Event Collaborations"]
  },
  {
    id: 6,
    companyName: "CloudSecure Systems",
    companyDescription: "Enterprise cybersecurity solutions protecting businesses from digital threats",
    logo: "https://images.unsplash.com/photo-1731012189558-c2d035998542",
    ownerName: "Robert Kim",
    ownerTitle: "CTO & Co-Founder",
    profileImage: "https://images.pexels.com/photos/3714743/pexels-photo-3714743.jpeg",
    serviceAreas: ["Seattle", "Portland", "Vancouver"],
    industry: "Cybersecurity",
    yearsInBusiness: 6,
    seekingPartnership: "National",
    partnerships: ["Strategic Alliances", "Joint Ventures", "Incubator/Accelerator Collaborations"]
  },
  {
    id: 7,
    companyName: "Sustainable Supply Chain",
    companyDescription: "Eco-friendly supply chain optimization for environmentally conscious companies",
    logo: "https://images.pexels.com/photos/3689532/pexels-photo-3689532.jpeg",
    ownerName: "Maria Gonzalez",
    ownerTitle: "Operations Director",
    profileImage: "https://images.pexels.com/photos/2381069/pexels-photo-2381069.jpeg",
    serviceAreas: ["Denver", "Phoenix", "Salt Lake City"],
    industry: "Supply Chain Management",
    yearsInBusiness: 7,
    seekingPartnership: "National",
    partnerships: ["Strategic Alliances", "Co-Branding", "Event Collaborations"]
  },
  {
    id: 8,
    companyName: "AI Learning Platform",
    companyDescription: "Machine learning education platform for professionals and businesses",
    logo: "https://images.pexels.com/photos/9973170/pexels-photo-9973170.jpeg",
    ownerName: "Alex Johnson",
    ownerTitle: "Chief Education Officer",
    profileImage: "https://images.pexels.com/photos/7433822/pexels-photo-7433822.jpeg",
    serviceAreas: ["Austin", "Dallas", "Houston"],
    industry: "Education Technology",
    yearsInBusiness: 1,
    seekingPartnership: "National",
    partnerships: ["Joint Ventures", "Incubator/Accelerator Collaborations", "Affiliate Partnerships"]
  }
];

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [matches, setMatches] = useState([]);
  const [activeTab, setActiveTab] = useState('matchmaker');
  const [messages, setMessages] = useState([]);
  const [deals, setDeals] = useState([]);
  const [swipeDirection, setSwipeDirection] = useState('');
  const [showAddDealModal, setShowAddDealModal] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const cardRef = useRef(null);

  // Calculate match probability based on partnership compatibility
  const calculateMatchProbability = (business1, business2) => {
    let score = 0;
    
    // Partnership type compatibility
    const commonPartnerships = business1.partnerships.filter(p => 
      business2.partnerships.includes(p)
    );
    score += commonPartnerships.length * 25;
    
    // Geographic compatibility
    if (business1.seekingPartnership === business2.seekingPartnership) score += 20;
    
    // Industry synergy (some industries work well together)
    const synergies = {
      'Technology': ['Marketing & Advertising', 'Financial Technology', 'Education Technology'],
      'Marketing & Advertising': ['Technology', 'Health & Wellness', 'Supply Chain Management'],
      'Financial Technology': ['Technology', 'Cybersecurity'],
      'Cybersecurity': ['Technology', 'Financial Technology'],
      'Health & Wellness': ['Marketing & Advertising', 'Supply Chain Management']
    };
    
    if (synergies[business1.industry]?.includes(business2.industry)) score += 20;
    
    // Experience level compatibility
    const exp1 = business1.yearsInBusiness;
    const exp2 = business2.yearsInBusiness;
    if (Math.abs(exp1 - exp2) <= 3) score += 15;
    
    return Math.min(score, 100);
  };

  // Generate special badges based on matching criteria
  const generateBadge = (business1, business2) => {
    const exp1 = business1.yearsInBusiness;
    const exp2 = business2.yearsInBusiness;
    
    if (business1.ownerTitle.includes('CEO') && business2.ownerTitle.includes('CEO')) {
      if (exp1 <= 5 && exp2 <= 5) {
        return { name: 'Boss Babies', description: 'Both CEOs with companies under 5 years' };
      }
      return { name: 'Power CEOs', description: 'Two visionary leaders unite' };
    }
    
    if (business1.industry === business2.industry) {
      return { name: 'Industry Twins', description: 'Same industry powerhouses' };
    }
    
    const commonPartnerships = business1.partnerships.filter(p => 
      business2.partnerships.includes(p)
    );
    
    if (commonPartnerships.includes('Strategic Alliances')) {
      return { name: 'Alliance Masters', description: 'Strategic partnership specialists' };
    }
    
    if (commonPartnerships.includes('Joint Ventures')) {
      return { name: 'Venture Partners', description: 'Joint venture enthusiasts' };
    }
    
    return { name: 'Perfect Match', description: 'Great partnership potential' };
  };

  const handleSwipe = useCallback((direction) => {
    if (currentIndex >= mockBusinesses.length) return;
    
    setSwipeDirection(direction);
    
    setTimeout(() => {
      if (direction === 'right') {
        // Create a match with probability and badge
        const currentBusiness = mockBusinesses[currentIndex];
        const matchBusiness = mockBusinesses[(currentIndex + 1) % mockBusinesses.length];
        const probability = calculateMatchProbability(currentBusiness, matchBusiness);
        const badge = generateBadge(currentBusiness, matchBusiness);
        
        const newMatch = {
          id: Date.now(),
          business: currentBusiness,
          matchedWith: matchBusiness,
          probability,
          badge,
          timestamp: new Date().toISOString()
        };
        
        setMatches(prev => [newMatch, ...prev]);
      }
      
      setCurrentIndex(prev => prev + 1);
      setSwipeDirection('');
    }, 300);
  }, [currentIndex]);

  const addMessage = (matchId, message) => {
    const newMessage = {
      id: Date.now(),
      matchId,
      message,
      timestamp: new Date().toISOString(),
      sender: 'user'
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const addDeal = (dealDetails) => {
    const newDeal = {
      id: Date.now(),
      ...dealDetails,
      timestamp: new Date().toISOString()
    };
    setDeals(prev => [newDeal, ...prev]);
    setShowAddDealModal(false);
    setSelectedMatch(null);
  };

  // Calculate leaderboard stats
  const getLeaderboardStats = () => {
    // Match leaders
    const matchCounts = {};
    matches.forEach(match => {
      const company = match.business.companyName;
      matchCounts[company] = (matchCounts[company] || 0) + 1;
    });

    // Deal leaders  
    const dealCounts = {};
    const dealValues = {};
    deals.forEach(deal => {
      const company = deal.companyName || 'Your Company';
      dealCounts[company] = (dealCounts[company] || 0) + 1;
      
      // Extract numeric value from deal value string
      const value = parseFloat(deal.dealValue?.replace(/[$,]/g, '') || 0);
      dealValues[company] = (dealValues[company] || 0) + value;
    });

    const matchLeaders = Object.entries(matchCounts)
      .map(([company, count]) => ({ company, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    const dealLeaders = Object.entries(dealCounts)
      .map(([company, count]) => ({ 
        company, 
        count, 
        totalValue: dealValues[company] || 0 
      }))
      .sort((a, b) => b.count - a.count || b.totalValue - a.totalValue)
      .slice(0, 5);

    return { matchLeaders, dealLeaders };
  };

  const currentBusiness = mockBusinesses[currentIndex];

  const renderMatchmaker = () => {
    if (currentIndex >= mockBusinesses.length) {
      return (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">🎉</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">You've seen all businesses!</h2>
            <p className="text-gray-600">Check your matches in the sidebar</p>
            <button 
              onClick={() => setCurrentIndex(0)}
              className="mt-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white px-6 py-2 rounded-full hover:shadow-lg transition-all"
            >
              Start Over
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="relative w-full max-w-md">
          {/* Business Card */}
          <div 
            ref={cardRef}
            className={`business-card ${swipeDirection ? `swipe-${swipeDirection}` : ''} 
              bg-white rounded-3xl shadow-2xl overflow-hidden transform transition-all duration-300 hover:scale-105`}
          >
            {/* Header with Company Logo and Info */}
            <div className="relative h-48 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6">
              <div className="flex items-start justify-between text-white">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-1">{currentBusiness.companyName}</h2>
                  <p className="text-sm opacity-90 leading-relaxed">{currentBusiness.companyDescription}</p>
                </div>
                <img 
                  src={currentBusiness.logo} 
                  alt="Company Logo"
                  className="w-16 h-16 rounded-xl bg-white/20 object-cover ml-4"
                />
              </div>
            </div>

            {/* Owner Profile */}
            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center space-x-4">
                <img 
                  src={currentBusiness.profileImage} 
                  alt={currentBusiness.ownerName}
                  className="w-16 h-16 rounded-full object-cover ring-4 ring-purple-100"
                />
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{currentBusiness.ownerName}</h3>
                  <p className="text-purple-600 font-medium">{currentBusiness.ownerTitle}</p>
                </div>
              </div>
            </div>

            {/* Business Details */}
            <div className="p-6 space-y-4">
              {/* Industry & Experience */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Industry</p>
                  <p className="text-sm font-semibold text-gray-800">{currentBusiness.industry}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Experience</p>
                  <p className="text-sm font-semibold text-gray-800">{currentBusiness.yearsInBusiness} years</p>
                </div>
              </div>

              {/* Service Areas */}
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Service Areas</p>
                <div className="flex flex-wrap gap-2">
                  {currentBusiness.serviceAreas.map((area, index) => (
                    <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                      {area}
                    </span>
                  ))}
                </div>
              </div>

              {/* Partnership Scope */}
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Partnership Scope</p>
                <span className={`px-3 py-1 text-sm rounded-full ${
                  currentBusiness.seekingPartnership === 'National' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-orange-100 text-orange-800'
                }`}>
                  {currentBusiness.seekingPartnership}
                </span>
              </div>

              {/* Partnership Interests */}
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Partnership Interests</p>
                <div className="grid grid-cols-1 gap-2">
                  {currentBusiness.partnerships.map((partnership, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">{partnership}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Swipe Buttons */}
          <div className="flex justify-center space-x-8 mt-8">
            <button 
              onClick={() => handleSwipe('left')}
              className="w-16 h-16 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white text-2xl transition-all hover:scale-110 shadow-lg"
            >
              ✕
            </button>
            <button 
              onClick={() => handleSwipe('right')}
              className="w-16 h-16 bg-green-500 hover:bg-green-600 rounded-full flex items-center justify-center text-white text-2xl transition-all hover:scale-110 shadow-lg"
            >
              ♥
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderMessages = () => (
    <div className="flex-1 p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Messages</h2>
      {matches.length === 0 ? (
        <div className="text-center text-gray-500 mt-12">
          <div className="text-6xl mb-4">💬</div>
          <p>No matches yet. Start swiping to find potential partners!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {matches.map((match) => (
            <div key={match.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <img 
                  src={match.business.profileImage} 
                  alt={match.business.ownerName}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <h3 className="font-semibold">{match.business.companyName}</h3>
                  <p className="text-sm text-gray-600">{match.business.ownerName}</p>
                </div>
                <div className="ml-auto">
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    match.badge.name === 'Boss Babies' ? 'bg-yellow-100 text-yellow-800' :
                    match.badge.name === 'Power CEOs' ? 'bg-purple-100 text-purple-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {match.badge.name}
                  </span>
                </div>
              </div>
              <div className="text-sm text-gray-700">
                <p>Match Probability: <span className="font-semibold text-green-600">{match.probability}%</span></p>
                <p className="mt-1">{match.badge.description}</p>
              </div>
              <div className="mt-4">
                <input 
                  type="text" 
                  placeholder="Send a message..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && e.target.value.trim()) {
                      addMessage(match.id, e.target.value);
                      e.target.value = '';
                    }
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderLeaderboard = () => (
    <div className="flex-1 p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Leaderboard</h2>
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4">
          <h3 className="text-xl font-semibold">Top Matchers This Month</h3>
        </div>
        <div className="p-6">
          {matches.length === 0 ? (
            <div className="text-center text-gray-500">
              <div className="text-6xl mb-4">🏆</div>
              <p>Start matching to see your ranking!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {matches.slice(0, 5).map((match, index) => (
                <div key={match.id} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                    index === 0 ? 'bg-yellow-500' : 
                    index === 1 ? 'bg-gray-400' : 
                    index === 2 ? 'bg-orange-600' : 'bg-blue-500'
                  }`}>
                    {index + 1}
                  </div>
                  <img 
                    src={match.business.profileImage} 
                    alt={match.business.ownerName}
                    className="w-10 h-10 rounded-full object-cover"
                  />
                  <div className="flex-1">
                    <p className="font-semibold">{match.business.companyName}</p>
                    <p className="text-sm text-gray-600">{match.probability}% match probability</p>
                  </div>
                  <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
                    {match.badge.name}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const renderDeals = () => (
    <div className="flex-1 p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Deals Closed</h2>
        <button 
          onClick={() => {
            if (matches.length > 0) {
              const sampleDeal = {
                dealName: "Sample Partnership Deal",
                dealValue: "$50,000",
                partnershipType: "Strategic Alliance",
                description: "Successful collaboration project"
              };
              addDeal(matches[0].id, sampleDeal);
            }
          }}
          className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-2 rounded-full hover:shadow-lg transition-all"
          disabled={matches.length === 0}
        >
          + Add Deal
        </button>
      </div>
      
      {deals.length === 0 ? (
        <div className="text-center text-gray-500 mt-12">
          <div className="text-6xl mb-4">🤝</div>
          <p>No deals closed yet. Make some matches and close your first deal!</p>
        </div>
      ) : (
        <div className="grid gap-6">
          {deals.map((deal) => (
            <div key={deal.id} className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{deal.dealName}</h3>
                  <p className="text-green-600 font-bold text-lg">{deal.dealValue}</p>
                </div>
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                  {deal.partnershipType}
                </span>
              </div>
              <p className="text-gray-600 mb-3">{deal.description}</p>
              <p className="text-sm text-gray-500">
                Closed on {new Date(deal.timestamp).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderSettings = () => (
    <div className="flex-1 p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Settings</h2>
      <div className="max-w-2xl">
        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Partnership Preferences</h3>
            <div className="space-y-3">
              {["Strategic Alliances", "Joint Ventures", "Co-Branding", "Affiliate Partnerships", 
                "Sponsorship Agreements", "Event Collaborations", "Incubator/Accelerator Collaborations"].map((type) => (
                <label key={type} className="flex items-center space-x-3">
                  <input type="checkbox" defaultChecked className="h-4 w-4 text-purple-600 rounded" />
                  <span className="text-gray-700">{type}</span>
                </label>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Geographic Preference</h3>
            <div className="space-y-2">
              <label className="flex items-center space-x-3">
                <input type="radio" name="geographic" defaultChecked className="h-4 w-4 text-purple-600" />
                <span className="text-gray-700">Local Partnerships</span>
              </label>
              <label className="flex items-center space-x-3">
                <input type="radio" name="geographic" className="h-4 w-4 text-purple-600" />
                <span className="text-gray-700">National Partnerships</span>
              </label>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Notifications</h3>
            <div className="space-y-3">
              <label className="flex items-center space-x-3">
                <input type="checkbox" defaultChecked className="h-4 w-4 text-purple-600 rounded" />
                <span className="text-gray-700">New Match Notifications</span>
              </label>
              <label className="flex items-center space-x-3">
                <input type="checkbox" defaultChecked className="h-4 w-4 text-purple-600 rounded" />
                <span className="text-gray-700">Message Notifications</span>
              </label>
              <label className="flex items-center space-x-3">
                <input type="checkbox" className="h-4 w-4 text-purple-600 rounded" />
                <span className="text-gray-700">Deal Opportunity Alerts</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">A</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Alliyn: Business Matchmaker
                </h1>
                <p className="text-sm text-gray-500">Part of Obsidian Suites</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-purple-100 px-4 py-2 rounded-full">
                <span className="text-purple-600 font-semibold">{matches.length}</span>
                <span className="text-purple-600 text-sm">Matches</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-lg h-screen sticky top-0">
          <div className="p-6">
            <div className="space-y-2">
              {[
                { id: 'matchmaker', name: 'Matchmaker', icon: '💝' },
                { id: 'messages', name: 'Messages', icon: '💬' },
                { id: 'leaderboard', name: 'Leaderboard', icon: '🏆' },
                { id: 'deals', name: 'Deals Closed', icon: '🤝' },
                { id: 'settings', name: 'Settings', icon: '⚙️' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-all ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span className="text-xl">{tab.icon}</span>
                  <span className="font-medium">{tab.name}</span>
                  {tab.id === 'messages' && matches.length > 0 && (
                    <span className="ml-auto bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {matches.length}
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1">
          {activeTab === 'matchmaker' && renderMatchmaker()}
          {activeTab === 'messages' && renderMessages()}
          {activeTab === 'leaderboard' && renderLeaderboard()}
          {activeTab === 'deals' && renderDeals()}
          {activeTab === 'settings' && renderSettings()}
        </main>
      </div>
    </div>
  );
}

export default App;