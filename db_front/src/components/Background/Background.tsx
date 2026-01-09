import React from 'react';
import ColorBends from './ColorBends';
import { BackgroundBox } from './styles';

const Background: React.FC = () => {
  return (
    <BackgroundBox>
      <ColorBends
        rotation={-180}
        speed={0.2}
        scale={1}
        parallax={0.65}
        noise={0.03}
        transparent={false}
      />
    </BackgroundBox>
  );
};

export default Background;
