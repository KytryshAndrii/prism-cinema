import React from 'react';
import { CloseButtonBox, FormBox, SignInButton, SignInCloseIcon, SignInTextField } from './styles';
import { IconButton } from '@mui/material';

type tSignInFormProps = {
    isOpen: boolean;
    onClose: () => void;
}

const SignInForm: React.FC<tSignInFormProps> = ({ isOpen, onClose }) => {
    if (!isOpen) return null;
  return (
    <FormBox>
    <CloseButtonBox>
        <IconButton size="small" onClick={onClose}>
          <SignInCloseIcon/>
        </IconButton>
      </CloseButtonBox>
      <SignInTextField
        label="Username"
        variant="filled"
        size="small"
      />
      <SignInTextField
        label="Password"
        variant="filled"
        type="password"
        size="small"
      />
      <SignInButton variant="contained">
        SIGN IN
      </SignInButton>
    </FormBox>
  );
};

export default SignInForm;
