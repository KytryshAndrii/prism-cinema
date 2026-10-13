import React from 'react';
import { Dialog, TextField, IconButton, CircularProgress, Alert } from '@mui/material';
import { CloseIcon } from '../../../icons/icons';
import {
  Brand,
  SignDialogTitle,
  SignUpButton,
  SignUpButtonContainer,
  SignUpDialogContent,
} from './styles';
import { useSignUpModal } from './useSignUpModal';

type tSignUpModalProps = {
  isOpen: boolean;
  onClose: () => void;
};

const SignUpModal: React.FC<tSignUpModalProps> = ({ isOpen, onClose }) => {
  const { register, handleSubmit, onSubmit, errors, isLoading, errorMessage } =
    useSignUpModal(onClose);

  return (
    <Dialog open={isOpen} onClose={onClose}>
      <SignDialogTitle>
        <Brand>
          JOIN PRISM<span>.</span>CINEMA
        </Brand>
        <IconButton onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </SignDialogTitle>

      <form onSubmit={handleSubmit(onSubmit)}>
        <SignUpDialogContent>
          <TextField
            label="Username"
            variant="filled"
            {...register('login')}
            error={!!errors.login}
            helperText={errors.login?.message}
          />
          <TextField
            label="Email address"
            variant="filled"
            {...register('email')}
            error={!!errors.email}
            helperText={errors.email?.message}
          />
          <TextField
            label="Password"
            variant="filled"
            {...register('password')}
            error={!!errors.password}
            helperText={errors.password?.message}
          />
          <TextField
            label="Date of birth"
            placeholder="YYYY-MM-DD"
            variant="filled"
            {...register('dateOfBirth')}
            error={!!errors.dateOfBirth}
            helperText={errors.dateOfBirth?.message}
          />

          {errorMessage && (
            <Alert severity="error" sx={{ mt: 1 }}>
              {errorMessage}
            </Alert>
          )}

          <SignUpButtonContainer>
            <SignUpButton variant="contained" type="submit" disabled={isLoading}>
              {isLoading ? <CircularProgress size={22} /> : 'SIGN UP'}
            </SignUpButton>
          </SignUpButtonContainer>
        </SignUpDialogContent>
      </form>
    </Dialog>
  );
};

export default SignUpModal;
