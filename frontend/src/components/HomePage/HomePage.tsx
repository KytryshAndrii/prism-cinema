import type React from 'react';
import { CTAButton, HomeWrapper, ImageBox, OverlayText } from './styles';
import { Typography } from '@mui/material';
import image from '../../assets/home_page/home_page.jpg';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <HomeWrapper>
        <ImageBox>
          <img
            src={image}
            alt="Cinema scene"
            style={{ width: '100%', display: 'block', borderRadius: '1rem' }}
          />
          <OverlayText>
            <Typography variant="h4" fontWeight="bold">
              WELCOME TO PRISM<span>.</span>CINEMA
            </Typography>
            <Typography variant="h4" fontWeight="bold">
              ENJOY FILMS WITH US
            </Typography>
            <CTAButton variant="contained" onClick={() => navigate('/films')}>
              Get started - it’s free!
            </CTAButton>
          </OverlayText>
        </ImageBox>
      </HomeWrapper>
    </>
  );
};

export default HomePage;
