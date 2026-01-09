import { useMemo } from 'react';

export const useMainPageFilmsRender = () => {
  return useMemo(() => {
    return Array.from({ length: 20 }, (_, i) => ({
      id: i + 1,
      title: `Film ${i + 1}`,
      imageUrl: `src/assets/poster.jpg`, 
    }));
  }, []);
};
