import React from 'react';
import { Typography, IconButton } from '@mui/material';
import { UserListWrapper, UserInfo, UserRow, Mugshot, EditionPen } from './styles';
import { SearchBar } from '../styles';

export const UserList: React.FC = () => {
  const users = ['WILL_SMITH', 'WILL_SMITH', 'WILL_SMITH'];

  return (
    <UserListWrapper>
      <Typography variant="h5">USERS</Typography>
      <SearchBar placeholder="Search user..." />

      {users.map(user => (
        <UserRow key={user}>
          <UserInfo>
            <Mugshot />
            <Typography variant="body1">{user}</Typography>
          </UserInfo>
          <IconButton>
            <EditionPen sx={{ color: 'white' }} />
          </IconButton>
        </UserRow>
      ))}
    </UserListWrapper>
  );
};
