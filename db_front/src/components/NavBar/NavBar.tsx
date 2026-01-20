import type React from 'react';
import {
  Brand,
  NavbarBox,
  NavButtons,
  ToolbarStyled,
  SingleNavButton,
  BrandWithAvatarButtons,
  AdminCut,
  AdminStyleWrapper,
  AdminNavButton,
} from './styles';
import SignUpModal from './Register/SignUpModal';
import SignInForm from './Sign/SignInForm';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import type { AppState } from '../../store/store';
import { useAuthForms } from '../../context/AuthFormContext';
import UserDropdown from './UserDropdown/UserDropdown';
import SearchBar from './SearchBar/SearchBar';

const NavBar: React.FC = () => {
  const { isSignInOpen, isSignUpOpen, toggleSignInForm, toggleSignUpForm } = useAuthForms();

  const navigate = useNavigate();
  const { isUserAdmin, isLoggedIn, login } = useSelector((state: AppState) => state.user);

  return (
    <>
      <NavbarBox>
        <ToolbarStyled>
          <BrandWithAvatarButtons>
            <Brand
              onClick={() => {
                if (!isLoggedIn) navigate('/');
              }}
            >
              PRISM<span>.</span>CINEMA
            </Brand>
            {isLoggedIn ? (
              <AdminStyleWrapper>
                <UserDropdown userLogin={login || ''} />
                {isUserAdmin ? <AdminCut /> : <></>}
              </AdminStyleWrapper>
            ) : (
              <></>
            )}
          </BrandWithAvatarButtons>
          {isLoggedIn ? (
            <NavButtons>
              <SingleNavButton onClick={() => navigate('/likes')}>LIKES</SingleNavButton>
              <SingleNavButton onClick={() => navigate('/films')}>FILMS</SingleNavButton>
              {isUserAdmin ? (
                <AdminNavButton onClick={() => navigate('/admin_panel')}>ADMIN</AdminNavButton>
              ) : (
                <></>
              )}
              <SearchBar />
            </NavButtons>
          ) : isSignInOpen ? (
            <SignInForm isOpen={isSignInOpen} onClose={toggleSignInForm} />
          ) : (
            <NavButtons>
              <SingleNavButton onClick={toggleSignInForm}>SIGN IN</SingleNavButton>
              <SingleNavButton onClick={toggleSignUpForm}>CREATE ACCOUNT</SingleNavButton>
              <SingleNavButton onClick={() => navigate('/films')}>FILMS</SingleNavButton>
              <SingleNavButton onClick={() => navigate('/subscriptions')}>
                SUBSCRIPTIONS
              </SingleNavButton>
              <SearchBar />
            </NavButtons>
          )}
        </ToolbarStyled>
      </NavbarBox>

      <SignUpModal isOpen={isSignUpOpen} onClose={toggleSignUpForm} />
    </>
  );
};

export default NavBar;
