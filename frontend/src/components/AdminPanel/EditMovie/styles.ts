import { Box, TextField } from '@mui/material';
import { styled } from '@mui/system';

export const EditionRow = styled(TextField)({
  marginTop: '1rem',
  backgroundColor: '#dceeff',
  borderRadius: '0.4rem',
  fontWeight: 'bold',
});

export const TwoColumnRow = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: '1rem',
  width: '100%',

  '& > *': {
    flex: 1,
  },
}));
