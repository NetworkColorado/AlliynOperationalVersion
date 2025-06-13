import React, { useState, useRef, useCallback, useEffect } from 'react';
import './App.css';

// Popup ads for monetization
const adPopups = [
  {
    id: 'popup1',
    title: '🚀 Scale Your Business Fast!',
    description: 'Join 10,000+ entrepreneurs using our proven growth system',
    cta: 'Get 30% Off Today',
    image: 'https://images.unsplash.com/photo-1556745757-8d76bdb6984b',
    backgroundColor: 'from-blue-500 to-purple-600'
  },
  {
    id: 'popup2',
    title: '💰 Business Funding Available',
    description: 'Get up to $500K funding for your business expansion',
    cta: 'Apply in 5 Minutes',
    image: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f',
    backgroundColor: 'from-green-500 to-teal-600'
  },
  {
    id: 'popup3',
    title: '📈 Free Marketing Audit',
    description: 'Discover how to 3x your revenue with expert strategies',
    cta: 'Get Free Audit',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f',
    backgroundColor: 'from-orange-500 to-red-600'
  }
];

// Mock sponsor profiles for advertising revenue
const sponsorProfiles = [
  {
    id: 'sponsor1',
    type: 'sponsor',
    companyName: "Microsoft for Startups",
    companyDescription: "Get $150,000 in Azure credits, free Office 365, and startup support programs",
    logo: "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
    sponsorBadge: "Featured Sponsor",
    ctaText: "Apply for Program",
    ctaUrl: "#",
    backgroundColor: "from-blue-600 to-blue-800"
  },
  {
    id: 'sponsor2', 
    type: 'sponsor',
    companyName: "Stripe Atlas",
    companyDescription: "Start your company in minutes. Get a US bank account, incorporate in Delaware, and get your tax ID",
    logo: "https://images.unsplash.com/photo-1559526324-593bc073d938",
    sponsorBadge: "Startup Partner",
    ctaText: "Start Your Company",
    ctaUrl: "#",
    backgroundColor: "from-purple-600 to-indigo-800"
  },
  {
    id: 'sponsor3',
    type: 'sponsor', 
    companyName: "AWS Activate",
    companyDescription: "Get up to $100,000 in AWS credits, technical support, and training for your startup",
    logo: "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg",
    sponsorBadge: "Cloud Partner",
    ctaText: "Get AWS Credits",
    ctaUrl: "#",
    backgroundColor: "from-orange-600 to-yellow-600"
  }
];

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
  const [showConfetti, setShowConfetti] = useState(false);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [showAdPopup, setShowAdPopup] = useState(false);
  const [currentAdPopup, setCurrentAdPopup] = useState(null);
  const [showMatchTitle, setShowMatchTitle] = useState(false);
  const [currentMatchTitle, setCurrentMatchTitle] = useState('');
  const [profilePreviewMode, setProfilePreviewMode] = useState(false);
  
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(true);
  const [authMode, setAuthMode] = useState('signin'); // 'signin' or 'signup'
  const [liveProfiles, setLiveProfiles] = useState([...mockBusinesses]);
  
  // Account Management
  const [accountType, setAccountType] = useState('free'); // 'free' or 'premium'
  const [swipeCount, setSwipeCount] = useState(0);
  const [matchCount, setMatchCount] = useState(0);
  const [lastLockoutTime, setLastLockoutTime] = useState(null);
  const [isLockedOut, setIsLockedOut] = useState(false);
  
  const [userProfile, setUserProfile] = useState({
    companyName: "Your Company",
    companyDescription: "Enter your company description",
    logo: "",
    ownerName: "Your Name",
    ownerTitle: "Your Title",
    profileImage: "",
    serviceAreas: ["Your City"],
    industry: "Your Industry",
    yearsInBusiness: 1,
    seekingPartnership: "Local",
    partnerships: ["Strategic Alliances"]
  });
  const cardRef = useRef(null);

  // Check lockout status on component mount
  useEffect(() => {
    if (lastLockoutTime && accountType === 'free') {
      const now = new Date().getTime();
      const lockoutEnd = new Date(lastLockoutTime).getTime() + (24 * 60 * 60 * 1000); // 24 hours
      if (now < lockoutEnd) {
        setIsLockedOut(true);
      } else {
        setIsLockedOut(false);
        setSwipeCount(0);
        setMatchCount(0);
      }
    }
  }, [lastLockoutTime, accountType]);

  // Combine businesses and sponsors for swiping
  const allProfiles = [...liveProfiles];
  
  // Insert sponsors every 4-5 profiles for optimal ad exposure
  const getProfileAtIndex = (index) => {
    // Show sponsor every 4th profile
    if (index > 0 && index % 4 === 0 && sponsorProfiles.length > 0) {
      const sponsorIndex = Math.floor(index / 4) % sponsorProfiles.length;
      return sponsorProfiles[sponsorIndex];
    }
    return allProfiles[index % allProfiles.length];
  };

  const currentProfile = getProfileAtIndex(currentIndex);
  const isCurrentSponsor = currentProfile?.type === 'sponsor';

  // Authentication functions
  const handleSignUp = (formData) => {
    const newProfile = {
      id: Date.now(),
      companyName: formData.companyName,
      companyDescription: formData.companyDescription,
      logo: "",
      ownerName: formData.ownerName,
      ownerTitle: formData.ownerTitle,
      profileImage: "",
      serviceAreas: formData.serviceAreas.split(',').map(area => area.trim()),
      industry: formData.industry,
      yearsInBusiness: parseInt(formData.yearsInBusiness),
      seekingPartnership: formData.seekingPartnership,
      partnerships: formData.partnerships || ["Strategic Alliances"],
      email: formData.email
    };
    
    // Add to live profiles
    setLiveProfiles(prev => [...prev, newProfile]);
    
    // Update user profile
    setUserProfile(newProfile);
    
    // Authenticate user
    setIsAuthenticated(true);
    setShowAuthModal(false);
    
    alert('🎉 Welcome to Alliyn! Your profile is now live and ready for matching!');
  };

  const handleSignIn = (email, password) => {
    // Simulate sign-in (in real app, this would validate credentials)
    setIsAuthenticated(true);
    setShowAuthModal(false);
    alert('Welcome back to Alliyn!');
  };

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

  // Enhanced badge generation with more fun names and match titles
  const generateBadge = (business1, business2) => {
    const exp1 = business1.yearsInBusiness;
    const exp2 = business2.yearsInBusiness;
    
    // Title matches with fun names
    if (business1.ownerTitle.includes('CEO') && business2.ownerTitle.includes('CEO')) {
      if (exp1 <= 5 && exp2 <= 5) {
        return { 
          name: 'Boss Babies', 
          description: 'Both CEOs with companies under 5 years',
          matchTitle: '👶 Boss Babies in Action!'
        };
      }
      return { 
        name: 'Power Titans', 
        description: 'Two visionary CEO leaders unite',
        matchTitle: '👑 CEO Power Duo!'
      };
    }
    
    if (business1.ownerTitle.includes('Founder') && business2.ownerTitle.includes('Founder')) {
      return { 
        name: 'Dream Builders', 
        description: 'Two founders building the future',
        matchTitle: '🚀 Founder Force Unite!'
      };
    }
    
    if (business1.ownerTitle.includes('Director') && business2.ownerTitle.includes('Director')) {
      return { 
        name: 'Vision Masters', 
        description: 'Directors with aligned strategic vision',
        matchTitle: '🎯 Director Dynasty!'
      };
    }
    
    // Partnership scope matches
    if (business1.seekingPartnership === business2.seekingPartnership) {
      if (business1.seekingPartnership === 'National') {
        return { 
          name: 'National Champions', 
          description: 'Both seeking nationwide partnerships',
          matchTitle: '🌟 National Network Activated!'
        };
      } else {
        return { 
          name: 'Local Heroes', 
          description: 'Perfect local partnership match',
          matchTitle: '🏘️ Local Legends Connected!'
        };
      }
    }
    
    // Industry matches
    if (business1.industry === business2.industry) {
      const industryTitles = {
        'Technology': { name: 'Tech Twins', title: '💻 Tech Titans Collide!' },
        'Health & Medical': { name: 'Health Heroes', title: '🏥 Medical Mavericks!' },
        'Finance & Banking': { name: 'Money Masters', title: '💰 Finance Force!' },
        'Real Estate': { name: 'Property Pros', title: '🏘️ Real Estate Royalty!' },
        'Food & Beverage': { name: 'Culinary Champions', title: '🍽️ Food Empire Builders!' },
        'Automotive & Transportation': { name: 'Mobility Masters', title: '🚗 Transport Titans!' },
        'Content Creation and Photography': { name: 'Creative Collective', title: '📸 Content Kings!' }
      };
      
      const industryData = industryTitles[business1.industry] || { 
        name: 'Industry Twins', 
        title: '🏢 Industry Leaders Unite!' 
      };
      
      return { 
        name: industryData.name, 
        description: `Same industry powerhouses in ${business1.industry}`,
        matchTitle: industryData.title
      };
    }
    
    // Experience level matches
    if (Math.abs(exp1 - exp2) <= 2) {
      if (exp1 <= 3 && exp2 <= 3) {
        return { 
          name: 'Startup Squad', 
          description: 'Both early-stage entrepreneurs',
          matchTitle: '🌱 Startup Squad Assembled!'
        };
      } else if (exp1 >= 7 && exp2 >= 7) {
        return { 
          name: 'Veteran Alliance', 
          description: 'Experienced business leaders',
          matchTitle: '🏆 Veteran Powerhouse!'
        };
      } else {
        return { 
          name: 'Growth Partners', 
          description: 'Similar experience levels',
          matchTitle: '📈 Growth Gang Connected!'
        };
      }
    }
    
    // Partnership type matches
    const commonPartnerships = business1.partnerships.filter(p => 
      business2.partnerships.includes(p)
    );
    
    if (commonPartnerships.includes('Strategic Alliances')) {
      return { 
        name: 'Alliance Masters', 
        description: 'Strategic partnership specialists',
        matchTitle: '🤝 Strategic Alliance Activated!'
      };
    }
    
    if (commonPartnerships.includes('Joint Ventures')) {
      return { 
        name: 'Venture Partners', 
        description: 'Joint venture enthusiasts',
        matchTitle: '🚀 Venture Squad Ready!'
      };
    }
    
    if (commonPartnerships.includes('Co-Branding')) {
      return { 
        name: 'Brand Builders', 
        description: 'Co-branding collaboration experts',
        matchTitle: '🎨 Brand Builder Brigade!'
      };
    }
    
    if (commonPartnerships.includes('Event Collaborations')) {
      return { 
        name: 'Event Dynamos', 
        description: 'Event collaboration specialists',
        matchTitle: '🎉 Event Empire Builders!'
      };
    }
    
    return { 
      name: 'Perfect Match', 
      description: 'Great partnership potential',
      matchTitle: '✨ Perfect Partnership Found!'
    };
  };

  const canSwipe = () => {
    if (accountType === 'premium') return true;
    if (isLockedOut) return false;
    return swipeCount < 10 && matchCount < 1;
  };

  const handleSwipe = useCallback((direction) => {
    if (currentIndex >= allProfiles.length) return;
    
    // Check if user can swipe
    if (!canSwipe()) {
      if (accountType === 'free') {
        setShowUpgradeModal(true);
      }
      return;
    }
    
    setSwipeDirection(direction);
    
    // Increment swipe count for free users
    if (accountType === 'free') {
      setSwipeCount(prev => prev + 1);
    }
    
    // Show popup ads occasionally (every 5 swipes for engagement)
    if (currentIndex > 0 && currentIndex % 5 === 0 && Math.random() > 0.5) {
      const randomAd = adPopups[Math.floor(Math.random() * adPopups.length)];
      setCurrentAdPopup(randomAd);
      setShowAdPopup(true);
    }
    
    setTimeout(() => {
      if (direction === 'right') {
        // Only create matches for regular business profiles, not sponsors
        if (!isCurrentSponsor) {
          // Create a match with probability and badge
          const matchBusiness = allProfiles[(currentIndex + 1) % allProfiles.length];
          const probability = calculateMatchProbability(currentProfile, matchBusiness);
          const badge = generateBadge(currentProfile, matchBusiness);
          
          // Show match title first
          setCurrentMatchTitle(badge.matchTitle);
          setShowMatchTitle(true);
          
          // Then show confetti
          setTimeout(() => {
            setShowConfetti(true);
            setShowMatchTitle(false);
          }, 1500);
          
          setTimeout(() => setShowConfetti(false), 4500);
          
          // Increment match count for free users
          if (accountType === 'free') {
            setMatchCount(prev => prev + 1);
          }
          
          const newMatch = {
            id: Date.now(),
            business: currentProfile,
            matchedWith: matchBusiness,
            probability,
            badge,
            timestamp: new Date().toISOString()
          };
          
          setMatches(prev => [newMatch, ...prev]);
          
          // Check if free user should be locked out
          if (accountType === 'free' && (swipeCount + 1 >= 10 || matchCount + 1 >= 1)) {
            setLastLockoutTime(new Date().toISOString());
            setIsLockedOut(true);
          }
        } else {
          // For sponsor profiles, just show celebration without creating match
          setShowConfetti(true);
          setTimeout(() => setShowConfetti(false), 3000);
          setTimeout(() => {
            alert('Thanks for your interest! Check out their exclusive offer.');
          }, 1500);
        }
      }
      
      setCurrentIndex(prev => prev + 1);
      setSwipeDirection('');
    }, 300);
  }, [currentIndex, accountType, swipeCount, matchCount, isCurrentSponsor, allProfiles]);

  const upgradeToePremium = () => {
    setAccountType('premium');
    setSwipeCount(0);
    setMatchCount(0);
    setIsLockedOut(false);
    setLastLockoutTime(null);
    setShowUpgradeModal(false);
    alert('🎉 Welcome to Premium! Enjoy unlimited matching!');
  };

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

  const updateUserProfile = (updatedProfile) => {
    setUserProfile(updatedProfile);
  };

  const saveProfile = () => {
    // Validate required fields
    const requiredFields = {
      'Company Name': userProfile.companyName,
      'Company Description': userProfile.companyDescription,
      'Your Name': userProfile.ownerName,
      'Job Title': userProfile.ownerTitle,
      'Industry': userProfile.industry,
    };

    const missingFields = Object.entries(requiredFields)
      .filter(([name, value]) => !value || value.trim() === '')
      .map(([name]) => name);

    if (missingFields.length > 0) {
      alert(`❌ Please fill in the following required fields:\n• ${missingFields.join('\n• ')}`);
      return;
    }

    // Validate service areas
    if (!userProfile.serviceAreas || userProfile.serviceAreas.length === 0) {
      alert('❌ Please add at least one service area.');
      return;
    }

    // Validate partnership interests
    if (!userProfile.partnerships || userProfile.partnerships.length === 0) {
      alert('❌ Please select at least one partnership interest.');
      return;
    }

    try {
      // Update live profiles if this user exists in the system
      setLiveProfiles(prev => {
        const existingIndex = prev.findIndex(profile => profile.id === userProfile.id);
        if (existingIndex >= 0) {
          // Update existing profile
          const updatedProfiles = [...prev];
          updatedProfiles[existingIndex] = { ...userProfile };
          return updatedProfiles;
        } else {
          // Add new profile (shouldn't happen in normal flow, but good fallback)
          return [...prev, { ...userProfile, id: Date.now() }];
        }
      });

      alert('✅ Profile saved successfully! Your updated information will be visible to other users.');
      
      // Optional: Switch to preview mode after saving
      setProfilePreviewMode(true);
    } catch (error) {
      alert('❌ Error saving profile. Please try again.');
      console.error('Profile save error:', error);
    }
  };

  const discardProfileChanges = () => {
    if (confirm('Are you sure you want to discard all changes? This cannot be undone.')) {
      // Reset to the last saved state
      // In a real app, you'd fetch from the server or keep a backup
      alert('Changes discarded. Profile reset to last saved state.');
    }
  };

  const handleImageUpload = (file, type) => {
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file (PNG, JPG, GIF, etc.)');
      return;
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('Image size must be less than 5MB. Please choose a smaller image.');
      return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64Image = e.target.result;
      if (type === 'profile') {
        setUserProfile(prev => ({ ...prev, profileImage: base64Image }));
        alert('✅ Profile photo updated! Remember to save your changes.');
      } else if (type === 'logo') {
        setUserProfile(prev => ({ ...prev, logo: base64Image }));
        alert('✅ Company logo updated! Remember to save your changes.');
      }
    };
    reader.onerror = () => {
      alert('❌ Error reading the image file. Please try again.');
    };
    reader.readAsDataURL(file);
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

  const getLockoutTimeRemaining = () => {
    if (!lastLockoutTime) return '';
    const now = new Date().getTime();
    const lockoutEnd = new Date(lastLockoutTime).getTime() + (24 * 60 * 60 * 1000);
    const remaining = Math.max(0, lockoutEnd - now);
    
    const hours = Math.floor(remaining / (1000 * 60 * 60));
    const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${hours}h ${minutes}m`;
  };

  const renderAuthModal = () => {
    if (authMode === 'signup') {
      return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-2xl">A</span>
                </div>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Join Alliyn</h2>
                <p className="text-gray-600">Create your business profile and start matching!</p>
              </div>

              <form onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const data = {
                  email: formData.get('email'),
                  password: formData.get('password'),
                  ownerName: formData.get('ownerName'),
                  ownerTitle: formData.get('ownerTitle'),
                  companyName: formData.get('companyName'),
                  companyDescription: formData.get('companyDescription'),
                  industry: formData.get('industry'),
                  yearsInBusiness: formData.get('yearsInBusiness'),
                  seekingPartnership: formData.get('seekingPartnership'),
                  serviceAreas: formData.get('serviceAreas'),
                  partnerships: Array.from(formData.getAll('partnerships'))
                };
                handleSignUp(data);
              }} className="space-y-4">
                
                {/* Account Info */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input 
                    type="email" 
                    name="email"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <input 
                    type="password" 
                    name="password"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>

                {/* Personal Info */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                    <input 
                      type="text" 
                      name="ownerName"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                    <input 
                      type="text" 
                      name="ownerTitle"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                </div>

                {/* Company Info */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
                  <input 
                    type="text" 
                    name="companyName"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company Description</label>
                  <textarea 
                    name="companyDescription"
                    rows="2"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                  ></textarea>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                    <select 
                      name="industry"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      <option value="">Select industry</option>
                      <option value="Health & Medical">Health & Medical</option>
                      <option value="Retail">Retail</option>
                      <option value="Insurance">Insurance</option>
                      <option value="Real Estate">Real Estate</option>
                      <option value="Finance & Banking">Finance & Banking</option>
                      <option value="Technology">Technology</option>
                      <option value="Automotive & Transportation">Automotive & Transportation</option>
                      <option value="Energy & Utilities">Energy & Utilities</option>
                      <option value="Construction & Home Development">Construction & Home Development</option>
                      <option value="Food & Beverage">Food & Beverage</option>
                      <option value="Manufacturing">Manufacturing</option>
                      <option value="Education">Education</option>
                      <option value="Content Creation and Photography">Content Creation and Photography</option>
                      <option value="Hospitality & Leisure">Hospitality & Leisure</option>
                      <option value="Agriculture & Forestry">Agriculture & Forestry</option>
                      <option value="Consumer Goods">Consumer Goods</option>
                      <option value="Waste Management & Environmental Services">Waste Management & Environmental Services</option>
                      <option value="Marketing & Advertising">Marketing & Advertising</option>
                      <option value="Financial Technology">Financial Technology</option>
                      <option value="Cybersecurity">Cybersecurity</option>
                      <option value="Health & Wellness">Health & Wellness</option>
                      <option value="Supply Chain Management">Supply Chain Management</option>
                      <option value="Education Technology">Education Technology</option>
                      <option value="Renewable Energy">Renewable Energy</option>
                      <option value="Consulting">Consulting</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Years in Business</label>
                    <input 
                      type="number" 
                      name="yearsInBusiness"
                      min="0"
                      max="100"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Service Areas (comma-separated)</label>
                  <input 
                    type="text" 
                    name="serviceAreas"
                    placeholder="e.g., San Francisco, New York, Remote"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Partnership Scope</label>
                  <select 
                    name="seekingPartnership"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  >
                    <option value="Local">Local Partnerships</option>
                    <option value="National">National Partnerships</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Partnership Interests</label>
                  <div className="grid grid-cols-1 gap-2 max-h-32 overflow-y-auto">
                    {["Strategic Alliances", "Joint Ventures", "Co-Branding", "Affiliate Partnerships"].map((type) => (
                      <label key={type} className="flex items-center space-x-2">
                        <input 
                          type="checkbox" 
                          name="partnerships"
                          value={type}
                          className="h-3 w-3 text-purple-600 rounded"
                        />
                        <span className="text-xs text-gray-700">{type}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="flex space-x-3 pt-4">
                  <button 
                    type="button"
                    onClick={() => setAuthMode('signin')}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                  >
                    Sign In Instead
                  </button>
                  <button 
                    type="submit"
                    className="flex-1 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:shadow-lg transition-all text-sm font-medium"
                  >
                    Create Account
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      );
    }

    // Sign In Modal
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
          <div className="p-6">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold text-2xl">A</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Welcome Back</h2>
              <p className="text-gray-600">Sign in to continue matching with businesses</p>
            </div>

            <form onSubmit={(e) => {
              e.preventDefault();
              const formData = new FormData(e.target);
              handleSignIn(formData.get('email'), formData.get('password'));
            }} className="space-y-4">
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input 
                  type="email" 
                  name="email"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input 
                  type="password" 
                  name="password"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              <div className="flex space-x-3 pt-4">
                <button 
                  type="button"
                  onClick={() => setAuthMode('signup')}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Create Account
                </button>
                <button 
                  type="submit"
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:shadow-lg transition-all font-medium"
                >
                  Sign In
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  };

  const renderMatchmaker = () => {
    if (currentIndex >= allProfiles.length * 2) {
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

    // Show lockout screen for free users
    if (accountType === 'free' && isLockedOut) {
      return (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center bg-white rounded-lg shadow-xl p-8 max-w-md">
            <div className="text-6xl mb-4">⏰</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Free Limit Reached</h2>
            <p className="text-gray-600 mb-4">
              You've used your free daily limit (10 swipes or 1 match). 
              Upgrade to Premium for unlimited matching!
            </p>
            <div className="bg-gray-100 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-600">Time remaining: <span className="font-bold">{getLockoutTimeRemaining()}</span></p>
            </div>
            <button
              onClick={() => setShowUpgradeModal(true)}
              className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-8 py-3 rounded-full hover:shadow-lg transition-all font-bold"
            >
              Upgrade to Premium - $19.99
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="flex-1 flex items-center justify-center p-8 relative">
        {/* Free User Swipe Counter */}
        {accountType === 'free' && (
          <div className="absolute top-4 right-4 bg-white rounded-lg shadow-md p-4 z-10">
            <div className="text-center">
              <p className="text-sm text-gray-600">Free Account</p>
              <p className="text-xs text-gray-500">Swipes: {swipeCount}/10</p>
              <p className="text-xs text-gray-500">Matches: {matchCount}/1</p>
              <button
                onClick={() => setShowUpgradeModal(true)}
                className="mt-2 text-xs bg-yellow-500 text-white px-3 py-1 rounded-full hover:bg-yellow-600 transition-colors"
              >
                Upgrade
              </button>
            </div>
          </div>
        )}

        {/* Match Title Display */}
        {showMatchTitle && (
          <div className="fixed inset-0 pointer-events-none z-50 flex items-center justify-center">
            <div className="match-title bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-full shadow-2xl">
              <h3 className="text-2xl font-bold text-center">{currentMatchTitle}</h3>
            </div>
          </div>
        )}

        {/* Confetti Animation */}
        {showConfetti && (
          <div className="fixed inset-0 pointer-events-none z-50">
            <div className="confetti-container">
              {[...Array(50)].map((_, i) => (
                <div
                  key={i}
                  className="confetti-piece"
                  style={{
                    left: `${Math.random() * 100}%`,
                    animationDelay: `${Math.random() * 3}s`,
                    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b', '#6c5ce7'][Math.floor(Math.random() * 7)]
                  }}
                />
              ))}
            </div>
            <div className="fixed inset-0 flex items-center justify-center">
              <div className="match-celebration bg-white rounded-lg p-8 shadow-2xl">
                <div className="text-center">
                  <div className="text-6xl mb-4">🎉</div>
                  <h3 className="text-2xl font-bold text-gray-800 mb-2">It's a Match!</h3>
                  <p className="text-gray-600">Great partnership potential detected!</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="relative w-full max-w-md">
          {/* Sponsor Card */}
          {isCurrentSponsor ? (
            <div 
              ref={cardRef}
              className={`business-card ${swipeDirection ? `swipe-${swipeDirection}` : ''} 
                bg-white rounded-3xl shadow-2xl overflow-hidden transform transition-all duration-300 hover:scale-105`}
            >
              {/* Sponsor Header */}
              <div className={`relative h-48 bg-gradient-to-br ${currentProfile.backgroundColor} p-6`}>
                <div className="absolute top-4 right-4">
                  <span className="px-3 py-1 bg-white/20 text-white rounded-full text-xs font-bold backdrop-blur-sm">
                    {currentProfile.sponsorBadge}
                  </span>
                </div>
                <div className="flex items-start justify-between text-white">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold mb-1">{currentProfile.companyName}</h2>
                    <p className="text-sm opacity-90 leading-relaxed">{currentProfile.companyDescription}</p>
                  </div>
                  <img 
                    src={currentProfile.logo} 
                    alt="Sponsor Logo"
                    className="w-16 h-16 rounded-xl bg-white/20 object-cover ml-4"
                  />
                </div>
              </div>

              {/* Sponsor Content */}
              <div className="p-6">
                <div className="text-center">
                  <div className="bg-gradient-to-r from-green-100 to-blue-100 rounded-lg p-4 mb-4">
                    <h3 className="text-lg font-bold text-gray-800 mb-2">Exclusive Offer for Alliyn Members</h3>
                    <p className="text-sm text-gray-600">Join thousands of successful businesses already using this platform</p>
                  </div>
                  
                  <button className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white py-3 px-6 rounded-lg font-bold text-lg hover:shadow-lg transition-all">
                    {currentProfile.ctaText}
                  </button>
                  
                  <p className="text-xs text-gray-500 mt-3">
                    Sponsored content • Learn more about partnership opportunities
                  </p>
                </div>
              </div>
            </div>
          ) : (
            /* Regular Business Card */
            <div 
              ref={cardRef}
              className={`business-card ${swipeDirection ? `swipe-${swipeDirection}` : ''} 
                bg-white rounded-3xl shadow-2xl overflow-hidden transform transition-all duration-300 hover:scale-105`}
            >
              {/* Header with Company Logo and Info */}
              <div className="relative h-48 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6">
                <div className="flex items-start justify-between text-white">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold mb-1">{currentProfile.companyName}</h2>
                    <p className="text-sm opacity-90 leading-relaxed">{currentProfile.companyDescription}</p>
                  </div>
                  <img 
                    src={currentProfile.logo} 
                    alt="Company Logo"
                    className="w-16 h-16 rounded-xl bg-white/20 object-cover ml-4"
                  />
                </div>
              </div>

              {/* Owner Profile */}
              <div className="p-6 border-b border-gray-100">
                <div className="flex items-center space-x-4">
                  <img 
                    src={currentProfile.profileImage} 
                    alt={currentProfile.ownerName}
                    className="w-16 h-16 rounded-full object-cover ring-4 ring-purple-100"
                  />
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800">{currentProfile.ownerName}</h3>
                    <p className="text-purple-600 font-medium">{currentProfile.ownerTitle}</p>
                  </div>
                </div>
              </div>

              {/* Business Details */}
              <div className="p-6 space-y-4">
                {/* Industry & Experience */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Industry</p>
                    <p className="text-sm font-semibold text-gray-800">{currentProfile.industry}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3">
                    <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Experience</p>
                    <p className="text-sm font-semibold text-gray-800">{currentProfile.yearsInBusiness} years</p>
                  </div>
                </div>

                {/* Service Areas */}
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Service Areas</p>
                  <div className="flex flex-wrap gap-2">
                    {currentProfile.serviceAreas?.map((area, index) => (
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
                    currentProfile.seekingPartnership === 'National' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-orange-100 text-orange-800'
                  }`}>
                    {currentProfile.seekingPartnership}
                  </span>
                </div>

                {/* Partnership Interests */}
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Partnership Interests</p>
                  <div className="grid grid-cols-1 gap-2">
                    {currentProfile.partnerships?.map((partnership, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span className="text-sm text-gray-700">{partnership}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Swipe Buttons */}
          <div className="flex justify-center space-x-8 mt-8">
            <button 
              onClick={() => handleSwipe('left')}
              disabled={!canSwipe()}
              className={`w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl transition-all hover:scale-110 shadow-lg ${
                canSwipe() 
                  ? 'bg-red-500 hover:bg-red-600' 
                  : 'bg-gray-400 cursor-not-allowed'
              }`}
            >
              {isCurrentSponsor ? '⏭' : '✕'}
            </button>
            <button 
              onClick={() => handleSwipe('right')}
              disabled={!canSwipe()}
              className={`w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl transition-all hover:scale-110 shadow-lg ${
                canSwipe() 
                  ? 'bg-green-500 hover:bg-green-600' 
                  : 'bg-gray-400 cursor-not-allowed'
              }`}
            >
              {isCurrentSponsor ? '📞' : '🤝'}
            </button>
          </div>
          
          {/* Advertisement Banner */}
          <div className="mt-8 bg-white rounded-lg shadow-md p-4 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h4 className="font-semibold text-gray-800 text-sm">Sponsored by TechCorp Solutions</h4>
                <p className="text-xs text-gray-600">Enterprise software solutions for growing businesses</p>
              </div>
              <button className="bg-blue-500 text-white px-4 py-2 rounded text-xs hover:bg-blue-600 transition-colors">
                Learn More
              </button>
            </div>
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
                    match.badge.name === 'Power Titans' ? 'bg-purple-100 text-purple-800' :
                    match.badge.name === 'Dream Builders' ? 'bg-blue-100 text-blue-800' :
                    match.badge.name === 'National Champions' ? 'bg-green-100 text-green-800' :
                    match.badge.name === 'Local Heroes' ? 'bg-orange-100 text-orange-800' :
                    'bg-indigo-100 text-indigo-800'
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

  const renderLeaderboard = () => {
    const { matchLeaders, dealLeaders } = getLeaderboardStats();
    
    return (
      <div className="flex-1 p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Leaderboard</h2>
        
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Match Leaders */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4">
              <h3 className="text-xl font-semibold flex items-center">
                <span className="mr-2">💝</span>
                Top Matchers This Month
              </h3>
            </div>
            <div className="p-6">
              {matchLeaders.length === 0 ? (
                <div className="text-center text-gray-500">
                  <div className="text-4xl mb-4">🤝</div>
                  <p>Start matching to see rankings!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {matchLeaders.map((leader, index) => (
                    <div key={leader.company} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                        index === 0 ? 'bg-yellow-500' : 
                        index === 1 ? 'bg-gray-400' : 
                        index === 2 ? 'bg-orange-600' : 'bg-blue-500'
                      }`}>
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold">{leader.company}</p>
                        <p className="text-sm text-gray-600">{leader.count} matches</p>
                      </div>
                      <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                        {leader.count} 🤝
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Deal Leaders */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white p-4">
              <h3 className="text-xl font-semibold flex items-center">
                <span className="mr-2">💰</span>
                Top Deal Closers
              </h3>
            </div>
            <div className="p-6">
              {dealLeaders.length === 0 ? (
                <div className="text-center text-gray-500">
                  <div className="text-4xl mb-4">🏆</div>
                  <p>Close your first deal to appear here!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {dealLeaders.map((leader, index) => (
                    <div key={leader.company} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                        index === 0 ? 'bg-green-500' : 
                        index === 1 ? 'bg-blue-400' : 
                        index === 2 ? 'bg-indigo-600' : 'bg-teal-500'
                      }`}>
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold">{leader.company}</p>
                        <p className="text-sm text-gray-600">{leader.count} deals • ${leader.totalValue.toLocaleString()}</p>
                      </div>
                      <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                        {leader.count} 💰
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Overall Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-3xl font-bold text-purple-600">{matches.length}</div>
            <div className="text-gray-600">Total Matches</div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-3xl font-bold text-green-600">{deals.length}</div>
            <div className="text-gray-600">Deals Closed</div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="text-3xl font-bold text-blue-600">
              ${deals.reduce((sum, deal) => sum + (parseFloat(deal.dealValue?.replace(/[$,]/g, '') || 0)), 0).toLocaleString()}
            </div>
            <div className="text-gray-600">Total Deal Value</div>
          </div>
        </div>

        {/* Featured Advertisement */}
        <div className="mt-8 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 rounded-lg shadow-lg overflow-hidden">
          <div className="p-6 text-white">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-2">🎯 Business Coaching Platform</h3>
                <p className="mb-4">Join 50,000+ entrepreneurs who've scaled their businesses with our proven methods</p>
                <div className="flex items-center space-x-4">
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">⭐ 4.9/5 Rating</span>
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">💰 Average 3x Revenue Growth</span>
                </div>
              </div>
              <div className="ml-6">
                <button className="bg-white text-orange-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-colors">
                  Start Free Trial
                </button>
                <p className="text-xs opacity-75 mt-2 text-center">Sponsored Content</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderDeals = () => (
    <div className="flex-1 p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Deals Closed</h2>
        <button 
          onClick={() => setShowAddDealModal(true)}
          className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-2 rounded-full hover:shadow-lg transition-all flex items-center space-x-2"
        >
          <span>+</span>
          <span>Add Deal</span>
        </button>
      </div>
      
      {deals.length === 0 ? (
        <div className="text-center text-gray-500 mt-12">
          <div className="text-6xl mb-4">🤝</div>
          <p className="text-lg mb-2">No deals closed yet!</p>
          <p className="text-sm">Click "Add Deal" to record your first successful partnership</p>
        </div>
      ) : (
        <div className="grid gap-6">
          {deals.map((deal) => (
            <div key={deal.id} className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{deal.dealName}</h3>
                  <p className="text-green-600 font-bold text-lg">{deal.dealValue}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    with <span className="font-medium">{deal.partnerCompany}</span>
                  </p>
                </div>
                <div className="text-right">
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                    {deal.partnershipType}
                  </span>
                  <p className="text-xs text-gray-500 mt-2">
                    {new Date(deal.timestamp).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <p className="text-gray-600 mb-3">{deal.description}</p>
              {deal.matchSource && (
                <div className="mt-3 p-3 bg-purple-50 rounded-lg">
                  <p className="text-sm text-purple-700">
                    <span className="font-medium">Match Source:</span> Found through {deal.matchSource}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Add Deal Modal */}
      {showAddDealModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-800">Add New Deal</h3>
                <button 
                  onClick={() => setShowAddDealModal(false)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>
              
              <form onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const dealDetails = {
                  dealName: formData.get('dealName'),
                  dealValue: formData.get('dealValue'),
                  partnerCompany: formData.get('partnerCompany'),
                  partnershipType: formData.get('partnershipType'),
                  description: formData.get('description'),
                  matchSource: formData.get('matchSource'),
                  companyName: formData.get('companyName') || 'Your Company'
                };
                addDeal(dealDetails);
              }} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Your Company Name
                  </label>
                  <input 
                    type="text" 
                    name="companyName"
                    placeholder="Enter your company name"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Deal Name
                  </label>
                  <input 
                    type="text" 
                    name="dealName"
                    placeholder="e.g., Marketing Partnership Agreement"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Deal Value
                  </label>
                  <input 
                    type="text" 
                    name="dealValue"
                    placeholder="e.g., $50,000"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Partner Company
                  </label>
                  <input 
                    type="text" 
                    name="partnerCompany"
                    placeholder="Company you partnered with"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Partnership Type
                  </label>
                  <select 
                    name="partnershipType"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select partnership type</option>
                    <option value="Strategic Alliances">Strategic Alliances</option>
                    <option value="Joint Ventures">Joint Ventures</option>
                    <option value="Co-Branding">Co-Branding</option>
                    <option value="Affiliate Partnerships">Affiliate Partnerships</option>
                    <option value="Sponsorship Agreements">Sponsorship Agreements</option>
                    <option value="Event Collaborations">Event Collaborations</option>
                    <option value="Incubator/Accelerator Collaborations">Incubator/Accelerator Collaborations</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    How did you find this partner?
                  </label>
                  <select 
                    name="matchSource"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  >
                    <option value="">Select source (optional)</option>
                    <option value="Alliyn App Match">Alliyn App Match</option>
                    <option value="Networking Event">Networking Event</option>
                    <option value="Referral">Referral</option>
                    <option value="Cold Outreach">Cold Outreach</option>
                    <option value="Social Media">Social Media</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Deal Description
                  </label>
                  <textarea 
                    name="description"
                    placeholder="Brief description of the partnership deal..."
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                    required
                  ></textarea>
                </div>

                <div className="flex space-x-3 pt-4">
                  <button 
                    type="button"
                    onClick={() => setShowAddDealModal(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    className="flex-1 px-4 py-2 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-lg hover:shadow-lg transition-all"
                  >
                    Add Deal
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderProfile = () => (
    <div className="flex-1 p-8">
      <div className="flex items-center space-x-4 mb-6">
        <h2 className="text-3xl font-bold text-gray-800">My Profile</h2>
        {accountType === 'premium' && (
          <span className="px-4 py-2 bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-full text-sm font-bold flex items-center space-x-2">
            <span>⭐</span>
            <span>PREMIUM</span>
          </span>
        )}
        <button
          onClick={() => setProfilePreviewMode(!profilePreviewMode)}
          className={`px-4 py-2 rounded-lg transition-all ${
            profilePreviewMode 
              ? 'bg-purple-500 text-white' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          {profilePreviewMode ? '✏️ Edit Profile' : '👀 Preview Profile'}
        </button>
      </div>
      
      {profilePreviewMode ? (
        <div className="max-w-md mx-auto">
          <h3 className="text-xl font-bold text-center mb-6 text-purple-600">
            How others see your profile:
          </h3>
          <div className="business-card bg-white rounded-3xl shadow-2xl overflow-hidden">
            <div className="relative h-48 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6">
              <div className="flex items-start justify-between text-white">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-1">{userProfile.companyName}</h2>
                  <p className="text-sm opacity-90 leading-relaxed">{userProfile.companyDescription}</p>
                </div>
                {userProfile.logo ? (
                  <img 
                    src={userProfile.logo} 
                    alt="Company Logo"
                    className="w-16 h-16 rounded-xl bg-white/20 object-cover ml-4"
                  />
                ) : (
                  <div className="w-16 h-16 rounded-xl bg-white/20 ml-4 flex items-center justify-center">
                    <span className="text-white">🏢</span>
                  </div>
                )}
              </div>
            </div>

            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center space-x-4">
                {userProfile.profileImage ? (
                  <img 
                    src={userProfile.profileImage} 
                    alt={userProfile.ownerName}
                    className="w-16 h-16 rounded-full object-cover ring-4 ring-purple-100"
                  />
                ) : (
                  <div className="w-16 h-16 rounded-full bg-gray-200 ring-4 ring-purple-100 flex items-center justify-center">
                    <span className="text-2xl">👤</span>
                  </div>
                )}
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{userProfile.ownerName}</h3>
                  <p className="text-purple-600 font-medium">{userProfile.ownerTitle}</p>
                </div>
              </div>
            </div>

            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Industry</p>
                  <p className="text-sm font-semibold text-gray-800">{userProfile.industry}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Experience</p>
                  <p className="text-sm font-semibold text-gray-800">{userProfile.yearsInBusiness} years</p>
                </div>
              </div>

              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Service Areas</p>
                <div className="flex flex-wrap gap-2">
                  {userProfile.serviceAreas?.map((area, index) => (
                    <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                      {area}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Partnership Scope</p>
                <span className={`px-3 py-1 text-sm rounded-full ${
                  userProfile.seekingPartnership === 'National' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-orange-100 text-orange-800'
                }`}>
                  {userProfile.seekingPartnership}
                </span>
              </div>

              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Partnership Interests</p>
                <div className="grid grid-cols-1 gap-2">
                  {userProfile.partnerships?.map((partnership, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                      <span className="text-sm text-gray-700">{partnership}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="max-w-2xl mx-auto">
          <h3 className="text-xl font-bold text-center mb-8 text-purple-600">
            Edit Your Business Profile
          </h3>
          
          <div className="bg-white rounded-lg shadow-lg p-8 space-y-6">
            {/* Profile Images */}
            <div className="grid md:grid-cols-2 gap-8 pb-6 border-b">
              <div className="text-center">
                <h4 className="font-semibold text-gray-800 mb-4">Company Logo</h4>
                <div className="mb-4 flex justify-center">
                  {userProfile.logo ? (
                    <img src={userProfile.logo} alt="Logo" className="w-24 h-24 rounded-xl object-cover border-4 border-purple-100" />
                  ) : (
                    <div className="w-24 h-24 rounded-xl bg-gray-200 border-4 border-purple-100 flex items-center justify-center">
                      <span className="text-2xl">🏢</span>
                    </div>
                  )}
                </div>
                <label className="cursor-pointer bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 transition-colors inline-block">
                  <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e.target.files[0], 'logo')} />
                  📷 Upload
                </label>
              </div>
              <div className="text-center">
                <h4 className="font-semibold text-gray-800 mb-4">Your Photo</h4>
                <div className="mb-4 flex justify-center">
                  {userProfile.profileImage ? (
                    <img src={userProfile.profileImage} alt="Profile" className="w-24 h-24 rounded-full object-cover border-4 border-purple-100" />
                  ) : (
                    <div className="w-24 h-24 rounded-full bg-gray-200 border-4 border-purple-100 flex items-center justify-center">
                      <span className="text-2xl">👤</span>
                    </div>
                  )}
                </div>
                <label className="cursor-pointer bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 transition-colors inline-block">
                  <input type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e.target.files[0], 'profile')} />
                  📷 Upload
                </label>
              </div>
            </div>

            {/* Basic Information */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Your Name</label>
                <input 
                  type="text" 
                  value={userProfile.ownerName}
                  onChange={(e) => setUserProfile(prev => ({ ...prev, ownerName: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  placeholder="Your full name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                <input 
                  type="text" 
                  value={userProfile.ownerTitle}
                  onChange={(e) => setUserProfile(prev => ({ ...prev, ownerTitle: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., CEO, Founder"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
              <input 
                type="text" 
                value={userProfile.companyName}
                onChange={(e) => setUserProfile(prev => ({ ...prev, companyName: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                placeholder="Your company name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Company Description</label>
              <textarea 
                value={userProfile.companyDescription}
                onChange={(e) => setUserProfile(prev => ({ ...prev, companyDescription: e.target.value }))}
                rows="3"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 resize-none"
                placeholder="Describe what your company does..."
              ></textarea>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                <select 
                  value={userProfile.industry}
                  onChange={(e) => setUserProfile(prev => ({ ...prev, industry: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Select industry</option>
                  <option value="Technology">Technology</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Finance">Finance</option>
                  <option value="Marketing">Marketing</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Years in Business</label>
                <input 
                  type="number" 
                  min="0"
                  value={userProfile.yearsInBusiness}
                  onChange={(e) => setUserProfile(prev => ({ ...prev, yearsInBusiness: parseInt(e.target.value) || 0 }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Service Areas</label>
              <input 
                type="text" 
                value={userProfile.serviceAreas?.join(', ') || ''}
                onChange={(e) => setUserProfile(prev => ({ 
                  ...prev, 
                  serviceAreas: e.target.value.split(',').map(area => area.trim()).filter(area => area) 
                }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                placeholder="e.g., San Francisco, New York (comma-separated)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Partnership Scope</label>
              <div className="space-y-2">
                <label className="flex items-center space-x-3">
                  <input 
                    type="radio" 
                    name="scope"
                    value="Local"
                    checked={userProfile.seekingPartnership === 'Local'}
                    onChange={(e) => setUserProfile(prev => ({ ...prev, seekingPartnership: e.target.value }))}
                    className="h-4 w-4 text-purple-600"
                  />
                  <span>Local Partnerships</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input 
                    type="radio" 
                    name="scope"
                    value="National"
                    checked={userProfile.seekingPartnership === 'National'}
                    onChange={(e) => setUserProfile(prev => ({ ...prev, seekingPartnership: e.target.value }))}
                    className="h-4 w-4 text-purple-600"
                  />
                  <span>National Partnerships</span>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Partnership Interests</label>
              <div className="grid grid-cols-2 gap-2">
                {["Strategic Alliances", "Joint Ventures", "Co-Branding", "Affiliate Partnerships"].map((type) => (
                  <label key={type} className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      checked={userProfile.partnerships?.includes(type) || false}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setUserProfile(prev => ({ 
                            ...prev, 
                            partnerships: [...(prev.partnerships || []), type]
                          }));
                        } else {
                          setUserProfile(prev => ({ 
                            ...prev, 
                            partnerships: (prev.partnerships || []).filter(p => p !== type)
                          }));
                        }
                      }}
                      className="h-4 w-4 text-purple-600 rounded"
                    />
                    <span className="text-sm">{type}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="flex justify-between pt-6 border-t">
              <button 
                type="button"
                onClick={() => setProfilePreviewMode(true)}
                className="px-6 py-2 border border-purple-500 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors"
              >
                👀 Preview
              </button>
              <button 
                type="button"
                onClick={saveProfile}
                className="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:shadow-lg transition-all"
              >
                💾 Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderSettings = () => (
    <div className="flex-1 p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Settings</h2>
      <div className="max-w-2xl space-y-6">
        
        {/* Account Plan */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <span className="mr-2">💎</span>
            Account Plan
          </h3>
          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium text-gray-800">
                Current Plan: <span className={`${accountType === 'premium' ? 'text-yellow-600' : 'text-gray-600'}`}>
                  {accountType === 'premium' ? 'Premium ⭐' : 'Free'}
                </span>
              </p>
              {accountType === 'free' && (
                <p className="text-sm text-gray-500 mt-1">
                  Limited to 10 swipes or 1 match per day
                </p>
              )}
              {accountType === 'premium' && (
                <p className="text-sm text-green-600 mt-1">
                  ✓ Unlimited swipes and matches
                </p>
              )}
            </div>
            {accountType === 'free' && (
              <button
                onClick={() => setShowUpgradeModal(true)}
                className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-all font-bold"
              >
                Upgrade to Premium - $19.99
              </button>
            )}
          </div>
        </div>

        {/* Usage Stats for Free Users */}
        {accountType === 'free' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Daily Usage</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Swipes Today:</span>
                <span className="font-medium">{swipeCount}/10</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Matches Today:</span>
                <span className="font-medium">{matchCount}/1</span>
              </div>
              {isLockedOut && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <p className="text-red-700 text-sm">
                    ⏰ Locked out for: {getLockoutTimeRemaining()}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Preferences */}
        <div className="bg-white rounded-lg shadow-md p-6">
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
        
        <div className="bg-white rounded-lg shadow-md p-6">
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

        <div className="bg-white rounded-lg shadow-md p-6">
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

      {/* Upgrade Modal */}
      {showUpgradeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6">
              <div className="text-center mb-6">
                <div className="text-6xl mb-4">⭐</div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Upgrade to Premium</h3>
                <p className="text-gray-600">Unlock unlimited business matching!</p>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-700">Unlimited swipes per day</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-700">Unlimited matches</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-700">No 24-hour lockouts</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-700">Premium badge on profile</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-700">Priority customer support</span>
                </div>
              </div>

              <div className="text-center mb-6">
                <div className="text-3xl font-bold text-yellow-600 mb-2">$19.99</div>
                <p className="text-sm text-gray-500">One-time payment</p>
              </div>

              <div className="flex space-x-3">
                <button 
                  onClick={() => setShowUpgradeModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button 
                  onClick={upgradeToePremium}
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-lg hover:shadow-lg transition-all font-bold"
                >
                  Upgrade Now
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50">
      {/* Authentication Modal */}
      {!isAuthenticated && showAuthModal && renderAuthModal()}
      
      {/* Main App */}
      {isAuthenticated && (
        <>
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
                    <p className="text-sm text-gray-500">Obsidian Suites</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {accountType === 'premium' && (
                    <span className="px-3 py-1 bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-full text-xs font-bold flex items-center space-x-1">
                      <span>⭐</span>
                      <span>PREMIUM</span>
                    </span>
                  )}
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
            <nav className="w-64 bg-white shadow-lg h-screen sticky top-0 overflow-y-auto">
              <div className="p-6">
                <div className="space-y-2">
                  {[
                    { id: 'matchmaker', name: 'Matchmaker', icon: '💝' },
                    { id: 'messages', name: 'Messages', icon: '💬' },
                    { id: 'leaderboard', name: 'Leaderboard', icon: '🏆' },
                    { id: 'deals', name: 'Deals Closed', icon: '🤝' },
                    { id: 'profile', name: 'My Profile', icon: '👤' },
                    { id: 'sponsor', name: 'Become a Sponsor', icon: '💰' },
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
                
                {/* Sidebar Advertisement */}
                <div className="mt-8 bg-gradient-to-br from-green-100 to-blue-100 rounded-lg p-4 border border-green-200">
                  <div className="text-center">
                    <div className="text-2xl mb-2">💼</div>
                    <h4 className="font-bold text-sm text-gray-800 mb-2">Business Accelerator</h4>
                    <p className="text-xs text-gray-600 mb-3">Join our 12-week program and scale your business 10x</p>
                    <button className="w-full bg-green-500 text-white py-2 px-3 rounded text-xs font-medium hover:bg-green-600 transition-colors">
                      Apply Now
                    </button>
                    <p className="text-xs text-gray-400 mt-2">Ad</p>
                  </div>
                </div>

                {/* Second Ad */}
                <div className="mt-4 bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg p-4 border border-purple-200">
                  <div className="text-center">
                    <div className="text-2xl mb-2">🚀</div>
                    <h4 className="font-bold text-sm text-gray-800 mb-2">Startup Funding</h4>
                    <p className="text-xs text-gray-600 mb-3">Get connected with investors looking for your business</p>
                    <button className="w-full bg-purple-500 text-white py-2 px-3 rounded text-xs font-medium hover:bg-purple-600 transition-colors">
                      Get Funding
                    </button>
                    <p className="text-xs text-gray-400 mt-2">Sponsored</p>
                  </div>
                </div>
              </div>
            </nav>

            {/* Main Content */}
            <main className="flex-1">
              {activeTab === 'matchmaker' && renderMatchmaker()}
              {activeTab === 'messages' && renderMessages()}
              {activeTab === 'leaderboard' && renderLeaderboard()}
              {activeTab === 'deals' && renderDeals()}
              {activeTab === 'profile' && renderProfile()}
              {activeTab === 'settings' && renderSettings()}
            </main>
          </div>
        </>
      )}

      {/* Popup Advertisement Modal */}
      {showAdPopup && currentAdPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full overflow-hidden">
            <div className={`relative h-48 bg-gradient-to-r ${currentAdPopup.backgroundColor} p-6`}>
              <button 
                onClick={() => setShowAdPopup(false)}
                className="absolute top-4 right-4 text-white/80 hover:text-white text-2xl font-bold"
              >
                ×
              </button>
              <div className="text-white h-full flex flex-col justify-center">
                <h3 className="text-2xl font-bold mb-2">{currentAdPopup.title}</h3>
                <p className="text-white/90">{currentAdPopup.description}</p>
              </div>
            </div>
            <div className="p-6">
              <button className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-6 rounded-lg font-bold text-lg hover:shadow-lg transition-all mb-3">
                {currentAdPopup.cta}
              </button>
              <button 
                onClick={() => setShowAdPopup(false)}
                className="w-full text-gray-500 text-sm hover:text-gray-700 transition-colors"
              >
                Maybe later
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;