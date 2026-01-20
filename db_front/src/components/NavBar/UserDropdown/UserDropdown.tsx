import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Avatar } from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import {
  DownArrow,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  DropdownList,
  DropdownWrapper,
} from './styles';
import { UserAvatar } from '../styles';
import { useDispatch } from 'react-redux';
import { logOut } from '../../../store/userSlice';

type tUserDropdownProps = {
  userLogin: string;
};

const UserDropdown: React.FC<tUserDropdownProps> = ({ userLogin }) => {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const toggleDropdown = () => setOpen(prev => !prev);

  const handleNavigate = (path: string) => {
    setOpen(false);
    navigate(path);
  };

  const handleSignOut = () => {
    dispatch(logOut());
    setOpen(false);
    navigate('/');
  };

  return (
    <DropdownWrapper>
      <DropdownHeader onClick={toggleDropdown}>
        <UserAvatar>
          <Avatar src="src/assets/user_avatar/user_avatar.svg" alt="User Icon" />
        </UserAvatar>
        <span>{userLogin?.toUpperCase()}</span>
        <DownArrow>{open ? <ArrowDropUpIcon /> : <ArrowDropDownIcon />}</DownArrow>
      </DropdownHeader>

      {open && (
        <DropdownList>
          <DropdownItem onClick={() => handleNavigate('/profile')}>Profile</DropdownItem>
          <DropdownDivider />
          <DropdownItem onClick={() => handleNavigate('/subscriptions')}>
            Subscriptions
          </DropdownItem>
          <DropdownItem onClick={handleSignOut}>Sign Out</DropdownItem>
        </DropdownList>
      )}
    </DropdownWrapper>
  );
};

export default UserDropdown;
