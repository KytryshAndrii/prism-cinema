import { Box, Button, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

export const PageWrapper = styled(Box)({
  width: '100%',
  minHeight: '100vh',
  color: '#fff',
});

/* ===== TOP BACKDROP ===== */
export const BackdropWrapper = styled(Box)({
  position: 'relative',
  width: '100%',
  height: '55vh',
  minHeight: '20rem',
  overflow: 'hidden',
});

export const BackdropImage = styled('img')({
  width: '100%',
  height: '100%',
  objectFit: 'cover',
});

export const BackdropGradient = styled(Box)({
  position: 'absolute',
  inset: 0
});

export const ContentWrapper = styled(Box)({
  position: 'relative',
  marginTop: '-8rem',
  padding: '4rem 6vw',
  background:
    'linear-gradient(to bottom, rgba(0,0,0,0.9), rgba(0,0,0,0.95))',
  backdropFilter: 'blur(0.5rem)',
});

export const InfoGrid = styled(Box)({
  display: 'grid',
  width: '65%',
  gridTemplateColumns: 'auto 1fr',
  gap: '2.5rem',
  alignItems: 'flex-start',
});


export const Poster = styled('img')({
  width: '14rem',
  borderRadius: '0.6rem',
  boxShadow: '0 1rem 3rem rgba(0,0,0,0.7)',
});

export const Title = styled(Typography)({
  fontSize: '2.2rem',
  fontWeight: 700,
  marginBottom: '1rem',
});

export const Description = styled(Typography)({
  fontSize: '1rem',
  lineHeight: 1.6,
  maxWidth: '42rem',
  opacity: 0.9,
});


export const Actions = styled(Box)({
  marginTop: '1.5rem',
  display: 'flex',
  gap: '1rem',
});

export const ActionButton = styled(Button)({
  padding: '0.6rem 1.4rem',
  borderRadius: '0.5rem',
  fontWeight: 600,
});


export const TrailerWrapper = styled(Box)({
  margin: '4rem auto 0', 
  width: '75%',
  aspectRatio: '16 / 9',
  borderRadius: '0.8rem',
  overflow: 'hidden',
  boxShadow: '0 1rem 3rem rgba(0,0,0,0.6)',
});




export const ToggleRow = styled(Box)({
  display: "flex",
  gap: "2rem",
  marginTop: "1.5rem",
});

export const ToggleLabel = styled(Typography)<{ active?: boolean }>(
  ({ active }) => ({
    fontSize: "0.9rem",
    fontWeight: 600,
    cursor: "pointer",
    color: active ? "#00e676" : "#aaa",
    borderBottom: active ? "0.125rem solid #00e676" : "none",
  })
);

export const ChipsRow = styled(Box)({
  display: "flex",
  gap: "0.75rem",
  marginTop: "1rem",
  flexWrap: "wrap",
});

export const Chip = styled(Box)({
  padding: "0.4rem 0.8rem",
  borderRadius: "0.4rem",
  backgroundColor: "rgba(255,255,255,0.12)",
  fontSize: "0.9rem",
  cursor:'pointer'
});
