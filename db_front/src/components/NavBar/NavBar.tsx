import type React from "react";
import { Brand, NavbarBox, NavButtons, SearchInput, ToolbarStyled, SingleNavButton, BrandWithAvatarButtons, UserAvatar } from "./styles";
import SignUpModal from "./Register/SignUpModal";
import { useNavBar } from "./useNavBar";
import SignInForm from "./Sign/SignInForm";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import type { AppState } from "../../store/store";
import { Avatar} from "@mui/material";

const NavBar: React.FC = () => {

  const {  isSignUpOpen,
        isSignInOpen,
        toggleSignInForm,
        toggleSignUpForm
      } = useNavBar();

  const navigate = useNavigate();
  const { isLoggedIn, login } = useSelector((state: AppState) => state.user);

     return (
      <>
        <NavbarBox>
          <ToolbarStyled>
           <BrandWithAvatarButtons> 
            <Brand>
              PRISM<span>.</span>CINEMA
            </Brand>
            {isLoggedIn? 
              ( 
                <UserAvatar>
                  <Avatar
                    src="src/assets/user_avatar/user_avatar.svg"
                    alt="User Icon"
                  />
                  {login?.toUpperCase()}
                </UserAvatar>
              ): <></>}
            </BrandWithAvatarButtons>
           {isLoggedIn ? (
            <NavButtons>
              <SingleNavButton onClick={() => navigate("/likes")}>LIKES</SingleNavButton>
              <SingleNavButton onClick={() => navigate("/films")}>FILMS</SingleNavButton>
              <SearchInput placeholder="Search..." />
            </NavButtons>
          ) : isSignInOpen ? (
            <SignInForm isOpen={isSignInOpen} onClose={toggleSignInForm} />
          ) : (
            <NavButtons>
              <SingleNavButton onClick={toggleSignInForm}>SIGN IN</SingleNavButton>
              <SingleNavButton onClick={toggleSignUpForm}>CREATE ACCOUNT</SingleNavButton>
              <SingleNavButton onClick={() => navigate("/films")}>FILMS</SingleNavButton>
              <SearchInput placeholder="Search..." />
            </NavButtons>
          )}
        </ToolbarStyled>
      </NavbarBox>

      <SignUpModal isOpen={isSignUpOpen} onClose={toggleSignUpForm} />
    </>
  );
};

export default NavBar