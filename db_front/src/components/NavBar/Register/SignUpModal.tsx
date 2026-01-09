import React from 'react';
import {
  Dialog,
  TextField,
  IconButton,
} from '@mui/material';
import { CloseIcon } from '../../../icons/icons';
import { Brand, SignDialogTitle, SignUpButton, SignUpButtonContainer, SignUpDialogContent } from './styles';

type tSignUpModalProps = {
  isOpen: boolean;
  onClose: () => void;
};

const SignUpModal: React.FC<tSignUpModalProps> = ({ isOpen, onClose }) => {
  return (
    <Dialog open={isOpen} onClose={onClose}>
      <SignDialogTitle>
        <Brand>JOIN PRISM<span>.</span>CINEMA</Brand>
        <IconButton onClick={onClose}>
          <CloseIcon />
        </IconButton>
      </SignDialogTitle>
      <SignUpDialogContent >
        <TextField label="Email address" variant="filled" />
        <TextField label="Username" variant="filled" />
        <TextField label="Password" variant="filled" />
        <TextField label="Date of birth" variant="filled" />
        <SignUpButtonContainer>
          <SignUpButton variant="contained">
            SING UP
          </SignUpButton>
        </SignUpButtonContainer>
      </SignUpDialogContent>
    </Dialog>
  );
};

export default SignUpModal;
