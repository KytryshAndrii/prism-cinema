import { Box } from '@mui/material';
import { styled } from '@mui/system';

export const DropdownWrapper = styled(Box)({
  position: 'relative',
  display: 'flex',
  flexDirection: 'column',
  color: '#ffffff',
});

export const DropdownHeader = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: '0.5rem',
  background: 'transparent',
  border: 'none',
  fontWeight: 'bold',
  color: '#ffffff',
  cursor: 'pointer',
  padding: '0.5rem',
  borderRadius: '0.2rem',
  fontSize: '1rem',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
});

export const DownArrow = styled(Box)({
  display: 'flex',
  alignItems: 'center',
});

export const DropdownList = styled(Box)({
  position: 'absolute',
  top: '95%',
  left: 0,
  marginTop: '0.5rem',
  minWidth: '12rem',
  background: 'rgba(36, 36, 36, 1)',
  borderRadius: '0.3rem',
  boxShadow: '0 0.2rem 1rem rgba(0, 0, 0, 0.4)',
  padding: '0.5rem 0',
  listStyle: 'none',
  zIndex: 99,
});

export const DropdownItem = styled(Box)({
  padding: '0.75rem 1rem',
  color: '#ffffff',
  fontWeight: 500,
  cursor: 'pointer',
  textAlign: 'left',
  fontSize: '1rem',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
});

export const DropdownDivider = styled(Box)({
  height: '1px',
  backgroundColor: 'rgba(255, 255, 255, 0.15)',
  margin: '0.3rem 0',
});
