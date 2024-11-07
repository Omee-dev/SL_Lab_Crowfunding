import React, { useEffect, useState } from 'react';

const ParallaxHeader = ({ imageUrl = "/api/placeholder/1920/500", title = "IITB Crowdfunding" }) => {
  const [scrollPosition, setScrollPosition] = useState(0);
  
  useEffect(() => {
    const handleScroll = () => {
      const position = window.scrollY;
      setScrollPosition(position);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Calculate opacity based on scroll position
  // Max darkness at 300px scroll
  const darkness = Math.min(scrollPosition / 300, 0.7);

  return (
    <div className="relative w-full h-[500px]">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url(${imageUrl})`,
          backgroundAttachment: 'fixed',
          transform: `translateY(${scrollPosition * 0.5}px)`,
        }}
      />
      {/* Darkening overlay */}
      <div 
        className="absolute inset-0"
        style={{
          backgroundColor: `rgba(0, 0, 0, ${darkness})`,
          transition: 'background-color 0.1s ease-out',
        }}
      />
      {/* Content */}
      <div className="relative h-full flex items-center justify-center">
        <h1 
          className="text-4xl md:text-6xl font-georgia font-semibold text-gray-200 tracking-wide"
          style={{
            textShadow: '-1px 0 black, 0 1px black, 1px 0 black, 0 -1px black',
            fontVariant: 'small-caps',
          }}
        >
          {title}
        </h1>
      </div>
    </div>
  );
};

export default ParallaxHeader;