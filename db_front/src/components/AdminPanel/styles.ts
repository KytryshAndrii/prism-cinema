import { Box, Button, InputBase, TextField } from '@mui/material';
import { styled } from '@mui/system';

export const PanelWrapper = styled(Box)(() => ({
  display: 'flex',
  gap: '1.5rem',
  padding: '3rem',
  maxWidth: '70vw',
  height: 'auto',
  margin: '6rem auto',
  backgroundColor: 'rgba(0, 0, 0, 0.9)',
  borderRadius: '1rem',
  color: '#fff',
}));

export const LeftPanel = styled(Box)(() => ({
  flex: 1,
  padding: '1rem',
  display: 'flex',
  flexDirection: 'column',
}));

export const RightPanel = styled(Box)(() => ({
  flex: 1,
  padding: '1rem',
}));

export const ToggleContainer = styled(Box)(() => ({
  display: 'flex',
  justifyContent: 'space-between',
  marginBottom: '1rem',
}));

export const ToggleButton = styled(Button)<{ active?: boolean }>(({ active }) => ({
  flex: 1,
  margin: '0 0.25rem',
  backgroundColor: active ? '#007bff' : '#222',
  color: '#fff',
  '&:hover': {
    backgroundColor: '#0056b3',
  },
}));

export const FormWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
  padding: '0.5rem',
  color: '#fff',
}));

const inputHeight = '3.5rem';

export const FormInput = styled(TextField)(() => ({
  backgroundColor: '#e5f0ff',
  borderRadius: '0.4rem',

  '& .MuiInputBase-root': {
    height: inputHeight,
    fontSize: '0.95rem',
  },

  '& label': {
    fontSize: '0.8rem',
  },
}));

export const TwoColumnRow = styled(Box)(() => ({
  display: 'flex',
  gap: '1rem',
  width: '100%',

  '& > *': {
    flex: 1,
  },
}));

export const UploadButton = styled(Button)(() => ({
  height: inputHeight,
  backgroundColor: '#007bff',
  color: 'white',
  fontSize: '0.85rem',
  fontWeight: 600,
  borderRadius: '0.4rem',

  '&:hover': {
    backgroundColor: '#1d4ed8',
  },
}));

export const SaveButton = styled(Button)(() => ({
  marginTop: '1.5rem',
  alignSelf: 'flex-end',
  padding: '0.7rem 2.2rem',
  fontSize: '1.2rem',
  fontWeight: 700,
  borderRadius: '0.5rem',
  backgroundColor: '#16a34a',

  '&:hover': {
    backgroundColor: '#15803d',
  },

  '&:disabled': {
    backgroundColor: '#374151',
    color: '#9ca3af',
  },
}));

export const SearchBar = styled(InputBase)(() => ({
  backgroundColor: '#2c2c2c',
  color: 'white',
  padding: '0.3rem 0.8rem',
  borderRadius: '8px',
  margin: '0.5rem 0 1rem 0',
  width: '100%',
}));
