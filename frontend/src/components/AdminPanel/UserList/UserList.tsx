import React from 'react';
import { Typography, IconButton, Modal, Box, Button, Alert } from '@mui/material';
import { UserListWrapper, UserInfo, UserRow, Mugshot, ModalBox } from './styles';
import { SearchBar } from '../styles';
import { TrashBin } from '../DeleteMovie/styles';
import { useUserList } from './useUserList';

export const UserList: React.FC = () => {
  const {
    users,
    searchPhrase,
    handleSearchChange,
    openDeleteModal,
    cancelDelete,
    confirmDelete,
    userToDelete,
    alert,
    closeAlert,
  } = useUserList();

  return (
    <UserListWrapper>
      <Typography variant="h5">USERS</Typography>
        {alert && (
        <Alert severity={alert.type} onClose={closeAlert}>
          {alert.message}
        </Alert>
      )}
      <SearchBar
        placeholder="Search user..."
        value={searchPhrase}
        onChange={e => handleSearchChange(e.target.value)}
      />

      {users!.map(user => (
        <UserRow key={user.id}>
          <UserInfo>
            <Mugshot />
            <Typography variant="body1">{user.login}</Typography>
          </UserInfo>
          <IconButton onClick={() => openDeleteModal(user)}>
            <TrashBin />
          </IconButton>
        </UserRow>
      ))}

      <Modal open={!!userToDelete} onClose={cancelDelete}>
        <ModalBox>
          <Typography>
            Are you sure you want to delete{' '}
            <strong>{userToDelete?.login}</strong>?
          </Typography>
          <Box display="flex" justifyContent="space-between">
            <Button variant="contained" color="error" onClick={confirmDelete}>
              DELETE
            </Button>
            <Button variant="outlined" onClick={cancelDelete}>
              CANCEL
            </Button>
          </Box>
        </ModalBox>
      </Modal>
    </UserListWrapper>
  );
};
