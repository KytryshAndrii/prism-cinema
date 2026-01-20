import { Alert, Box, Button, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

export const Wrapper = styled(Box)({
  width: '100%',
  minHeight: '90vh',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
});

export const PlansContainer = styled(Box)({
  width: '75%',
  display: 'grid',
  gridTemplateColumns: 'repeat(3, 1fr)',
  borderRadius: '0.75rem',
  overflow: 'hidden',
  border: '0.15rem solid #1e88e5',
  backgroundColor: 'rgba(30, 30, 30, 0.85)',
  backdropFilter: 'blur(1.5rem)',
});

export const PlanCard = styled(Box)({
  padding: '2rem 1.5rem',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
  textAlign: 'center',
  borderRight: '0.0625rem solid rgba(255,255,255,0.15)',

  '&:last-child': {
    borderRight: 'none',
  },
});

export const Badge = styled(Box)<{ color: string }>(({ color }) => ({
  alignSelf: 'center',
  padding: '0.25rem 0.75rem',
  borderRadius: '1rem',
  backgroundColor: color,
  color: '#fff',
  fontWeight: 'bold',
  fontSize: '1.5rem',
  marginBottom: '1.5rem',
}));

export const Description = styled(Typography)({
  fontSize: '0.95rem',
  color: '#e0e0e0',
  lineHeight: 1.5,
  marginBottom: '2rem',
});

export const Price = styled(Box)({
  marginBottom: '1.5rem',
});

export const PriceCurrency = styled(Typography)({
  fontSize: '0.85rem',
  color: '#bdbdbd',
});

export const PriceValue = styled(Typography)({
  fontSize: '2.2rem',
  fontWeight: 700,
  color: '#ffffff',
});

export const SubscribeButton = styled(Button)({
  marginTop: '1.5rem',
  backgroundColor: '#1e88e5',
  color: '#fff',
  fontWeight: 700,
  borderRadius: '0.4rem',
  padding: '0.8rem 1.5rem',
  '&:hover': {
    backgroundColor: '#1565c0',
  },
});

export const AlertWrapper = styled(Alert)({
  width: '40%',
  marginTop: '1.5rem',
});

export const CurrentPlanText = styled(Typography)({
  fontWeight: 'bold',
  color: '#4caf50',
  marginTop: '4.5rem',
});
