import { Autocomplete, Box, Button, TextField } from '@mui/material';
import { styled } from '@mui/system';

export const Wrapper = styled(Box)(() => ({
  padding: '1.2rem',
  maxHeight: '85vh',
  overflowY: 'auto',
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
}));

export const Title = styled(Box)(() => ({
  fontSize: '1.5rem',
  fontWeight: 700,
  color: '#fff',
}));

export const FormInput = styled(TextField)(() => ({
  backgroundColor: '#e8f0fe',
  borderRadius: '0.4rem',
}));

export const TwoColumnRow = styled(Box)(() => ({
  display: 'flex',
  gap: '1rem',

  '& > *': {
    flex: 1,
  },
}));

export const UploadButton = styled(Button)(() => ({
  height: '3.5rem',
  fontWeight: 600,
}));

export const SaveButton = styled(Button)(() => ({
  marginTop: '1rem',
  height: '3.8rem',
  fontWeight: 700,
}));

export const StyledAutocomplete = styled(Autocomplete)(() => ({
  backgroundColor: '#e8f0fe',
  borderRadius: '0.4rem',
}));
