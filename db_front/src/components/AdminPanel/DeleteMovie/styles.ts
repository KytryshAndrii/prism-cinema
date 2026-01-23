import { Box, InputBase } from '@mui/material';
import { styled } from '@mui/system';
import { TrashBinIcon } from '../../../icons/icons';

export const SearchBar = styled(InputBase)(() => ({
  backgroundColor: '#2c2c2c',
  color: 'white',
  padding: '0.3rem 0.8rem',
  borderRadius: '0.5rem',
  margin: '0.5rem 0 1rem 0',
  width: '100%',
}));

export const MovieList = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

export const MovieItem = styled(Box)(() => ({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  backgroundColor: '#1c1c1c',
  color: 'white',
  padding: '0.5rem 1rem',
  marginBottom: '0.5rem',
  borderRadius: '0.5rem',
}));

export const TrashBin = styled(TrashBinIcon)({
  color: 'white',
});

export const ModalBox = styled(Box)({
  backgroundColor: '#121212',
  padding: '1.5rem',
  color: 'white',
  borderRadius: '1rem',
  width: '19rem',
  margin: '20vh auto',
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
});
