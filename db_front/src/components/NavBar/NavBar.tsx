import type React from "react";
import { Brand, NavbarBox, NavButtons, SearchInput, ToolbarStyled, SingleNavButton } from "./styles";
import SignUpModal from "./Register/SignUpModal";
import { useNavBar } from "./useNavBar";
import SignInForm from "./Sign/SignInForm";
import { useNavigate } from "react-router-dom";


const NavBar: React.FC = () => {

  const {  isSignUpOpen,
        isSignInOpen,
        toggleSignInForm,
        toggleSignUpForm} = useNavBar();

  const navigate = useNavigate();

     return (
      <>
        <NavbarBox>
          <ToolbarStyled>
            <Brand onClick={() => navigate("/")}>
              PRISM<span>.</span>CINEMA
            </Brand>
             {isSignInOpen ? (
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