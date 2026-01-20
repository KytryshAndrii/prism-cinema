import { Box, Button, DialogContent, DialogTitle } from '@mui/material';
import { styled } from '@mui/material/styles';

export const SignDialogTitle = styled(DialogTitle)({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
});

export const Brand = styled(Box)(() => ({
  fontWeight: 'semi-bold',
  span: {
    color: '#EE131F',
  },
}));

export const SignUpDialogContent = styled(DialogContent)({
  display: 'flex',
  flexDirection: 'column',
  gap: '2rem',
  minWidth: '25rem',
});

export const SignUpButtonContainer = styled(Box)({
  textAlign: 'center',
});

export const SignUpButton = styled(Button)({
  bgcolor: '#00C853',
  color: 'white',
  fontWeight: 'bold',
  borderRadius: '0.5rem',
  px: '2rem',
  py: '0.5rem',
  mt: '0.5rem',
});
