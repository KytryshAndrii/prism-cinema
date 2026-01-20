import React from 'react';
import { CloseButtonBox, FormBox, SignInButton, SignInCloseIcon, SignInTextField } from './styles';
import { Alert, CircularProgress, IconButton } from '@mui/material';
import { useSignIn } from './useSignIn';

type tSignInFormProps = {
  isOpen: boolean;
  onClose: () => void;
};

const SignInForm: React.FC<tSignInFormProps> = ({ isOpen, onClose }) => {
  const { register, handleSubmit, onSubmit, errors, isLoading, errorMessage } = useSignIn(onClose);

  if (!isOpen) return null;
  return (
    <FormBox onSubmit={handleSubmit(onSubmit)}>
      <CloseButtonBox>
        <IconButton size="small" onClick={onClose}>
          <SignInCloseIcon />
        </IconButton>
      </CloseButtonBox>

      <SignInTextField
        label="Username"
        variant="filled"
        size="small"
        {...register('login')}
        error={!!errors.login}
        helperText={errors.login?.message}
      />

      <SignInTextField
        label="Password"
        type="password"
        variant="filled"
        size="small"
        {...register('password')}
        error={!!errors.password}
        helperText={errors.password?.message}
      />

      {errorMessage && (
        <Alert severity="error" sx={{ mt: '0.5rem' }}>
          {errorMessage}
        </Alert>
      )}

      <SignInButton variant="contained" disabled={isLoading} onClick={handleSubmit(onSubmit)}>
        {isLoading ? <CircularProgress size={22} /> : 'SIGN IN'}
      </SignInButton>
    </FormBox>
  );
};

export default SignInForm;
