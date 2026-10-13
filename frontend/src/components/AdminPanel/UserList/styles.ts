import { Box } from '@mui/material';
import { styled } from '@mui/system';
import { AccountMugShot, EditPenIcon } from '../../../icons/icons';

export const UserListWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  padding: '0.5rem',
  color: '#fff',
  marginTop: '4rem',
}));

export const UserRow = styled(Box)(() => ({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  backgroundColor: '#1c1c1c',
  color: 'white',
  padding: '0.5rem 1rem',
  marginBottom: '0.5rem',
  borderRadius: '0.5rem',
}));

export const UserInfo = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
}));

export const Mugshot = styled(AccountMugShot)({
  color: 'white',
  marginRight: '0.5rem',
});

export const EditionPen = styled(EditPenIcon)({
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
