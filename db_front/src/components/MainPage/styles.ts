import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

export const Container = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  paddingTop: '5rem',
  width: '100%',
  minHeight: '100vh',
  background: `linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.5) 40%, rgba(0,0,0,0.2) 70%, rgba(0,0,0,0) 100%)`,
  backdropFilter: 'blur(1rem)',
});

export const Heading = styled('h2')({
  fontSize: '2rem',
  padding: '1rem',
  fontWeight: 'bold',
  backgroundColor: 'transparent',
  boxShadow: '0 0.125rem 0.625rem rgba(0, 0, 0, 0.5)',
  backdropFilter: 'blur(1.7rem)',
  borderRadius: '0.5rem', 
  color: '#ffffff',
  marginBottom: '3rem',
  textAlign: 'center',
});

export const FilmsGrid = styled(Box)({
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(10rem, 1fr))',
  gap: '1rem',
  width: '75%',
  justifyContent: 'center',
});

export const FilmCard = styled(Box)({
  cursor: 'pointer',
  borderRadius: '0.5rem',
  overflow: 'hidden',
  backgroundColor: '#111',
  boxShadow: '0 0.125rem 0.5rem rgba(0,0,0,0.5)',
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'scale(1.05)',
  },
});

export const FilmImage = styled('img')({
  width: '100%',
  height: 'auto',
  display: 'block',
});

export const FilmInfo = styled(Box)({
  padding: '0.5rem',
  backgroundColor: '#222',
});

export const FilmTitle = styled(Box)({
  fontSize: '1rem',
  color: '#fff',
  fontWeight: 'bold',
});
