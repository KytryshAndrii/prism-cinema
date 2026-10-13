import { styled } from '@mui/material/styles';

export const BackgroundBox = styled('div')({
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100vw',
  height: '100vh',
  zIndex: -1,
  pointerEvents: 'none',
  overflow: 'hidden',
});
