import { useState, useEffect } from 'react';
import { Dimensions } from 'react-native';

export default function useWindowDimensions() {
  const [dimensions, setDimensions] = useState({
    window: Dimensions.get('window'),
  });

  useEffect(() => {
    const subscription = Dimensions.addEventListener('change', ({ window }) => {
      setDimensions({ window });
    });
    
    return () => subscription.remove();
  }, []);

  return {
    width: dimensions.window.width,
    height: dimensions.window.height,
    isSmallScreen: dimensions.window.width < 768, // Define small screen threshold
  };
}