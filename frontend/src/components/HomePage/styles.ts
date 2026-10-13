import { styled } from '@mui/material/styles';
import { Box, Button } from '@mui/material';

export const HomeWrapper = styled(Box)({
  display: 'flex',
  height: '50%',
  flexDirection: 'column',
  alignItems: 'center',
  position: 'relative',
  justifyContent: 'flex-start',
  paddingTop: '10rem',
  zIndex: 1,
});

export const ImageBox = styled(Box)({
  position: 'relative',
  width: '80%',
  maxWidth: '50rem',
  borderRadius: '2rem',
  boxShadow: '0 1rem 2rem rgba(0, 0, 0, 0.4)',
});

export const OverlayText = styled(Box)({
  position: 'absolute',
  width: '80%',
  top: '27rem',
  left: '50%',
  transform: 'translateX(-50%)',
  color: '#fff',
  textAlign: 'center',
  textShadow: '0.12rem 0.12rem 0.25rem rgba(0,0,0,0.6)',
  span: {
    color: '#EE131F',
  },
});

export const CTAButton = styled(Button)({
  backgroundColor: '#00AC1C',
  color: '#fff',
  fontSize: '1.2rem',
  fontWeight: 'bold',
  padding: ' 1rem 2rem',
  borderRadius: '1rem',
  marginTop: '0.5rem',
  '&:hover': {
    backgroundColor: '#00AC1B',
  },
});
