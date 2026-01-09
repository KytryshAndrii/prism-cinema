import { useState } from 'react';

export const useNavBar = () => {
    const [isSignInOpen, setIsSignInOpen] = useState(false);
    const [isSignUpOpen, setIsSignUpOpen] = useState(false);

    const toggleSignInForm = (): void => {
        setIsSignInOpen(!isSignInOpen)
    }

    const toggleSignUpForm = (): void => {
        setIsSignUpOpen(!isSignUpOpen)
    }

    return {
        isSignUpOpen,
        isSignInOpen,
        toggleSignInForm,
        toggleSignUpForm
    };
}