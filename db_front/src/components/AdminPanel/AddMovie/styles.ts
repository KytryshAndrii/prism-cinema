import { Box, Button, TextField } from '@mui/material';
import { styled } from '@mui/system';

export const PanelWrapper = styled(Box)(() => ({
  display: 'flex',
  width: '100%',
  height: '100%',
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
  borderRadius: '6px',
}));
export const DeleteMovieWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

export const UserListWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

export const UserRow = styled(Box)(() => ({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  backgroundColor: '#1c1c1c',
  color: 'white',
  padding: '0.5rem 1rem',
  marginBottom: '0.5rem',
  borderRadius: '6px',
}));

export const UserInfo = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
}));

export const AdditionRow = styled(TextField)({
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
