import { Box, Button, TextField } from '@mui/material';
import { styled } from '@mui/material/styles';
import { CloseIcon } from '../../../icons/icons';

export const FormBox = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: '1rem',
});

export const SignInButton = styled(Button)({
    bgcolor: '#00C853',
    color: 'white',
    fontWeight: 'bold',
    borderRadius: '0.5rem',
    px: '1.5rem',
    py: '0.5rem',
})

export const SignInTextField = styled(TextField)({
    background: '#fff',
    borderRadius: '0.8rem'
})

export const CloseButtonBox = styled(Box)({
  top: '0.5rem',
  right: '0.5rem',
  zIndex: 10,
});

export const SignInCloseIcon = styled(CloseIcon)({
  color: '#fff'
})