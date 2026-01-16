import { AppBar, Toolbar, InputBase, Button, Box } from '@mui/material';
import { styled, alpha } from '@mui/material/styles';

export const NavbarBox = styled(AppBar)(() => ({
  backgroundColor: 'transparent',
  boxShadow: '0 0.125rem 0.625rem rgba(0, 0, 0, 0.3)',
  backdropFilter: 'blur(0.25rem)', 
  zIndex: 1000,
}));

export const ToolbarStyled = styled(Toolbar)({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: '0 2rem',
});


export const Brand = styled(Box)(() => ({
  fontSize: '1.4rem',
  fontWeight: 'bold',
  color: '#ffffff',
  span: {
    color: '#EE131F',
  },
  cursor: 'pointer'
}));

export const NavButtons = styled(Box)({
  display: 'flex',
  gap: '1rem',
  alignItems: 'center',
});

export const UserAvatar = styled(Box)({
  display:"flex",
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  gap: "1rem",
  color: '#fff',
  fontSize: '1.2rem',
  fontWeight: 'bold',
  cursor:"pointer"
})

export const BrandWithAvatarButtons = styled(Box)({
  display:"flex",
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  gap: "3rem"
})

export const SingleNavButton =  styled(Button)({
  color: '#fff',
  fontSize: '1rem',
  fontWeight: 'bold',
});

export const SearchInput = styled(InputBase)(() => ({
  backgroundColor: alpha('#ffffff', 0.1),
  padding: '0.375rem 0.75rem',
  borderRadius: '35rem',
  color: '#fff',
  border: '0.0625rem solid rgba(255,255,255,0.2)',
  fontSize: '0.9rem',
}));
