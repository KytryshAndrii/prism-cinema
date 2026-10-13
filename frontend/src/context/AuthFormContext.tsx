import React, { createContext, useContext, useState } from 'react';

type tAuthFormsContextType = {
  isSignInOpen: boolean;
  isSignUpOpen: boolean;
  pendingPlanId: string | null;
  toggleSignInForm: () => void;
  toggleSignUpForm: () => void;
  setPendingPlanId: (id: string | null) => void;
};

const AuthFormsContext = createContext<tAuthFormsContextType | undefined>(undefined);

export const AuthFormsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isSignInOpen, setIsSignInOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const [pendingPlanId, setPendingPlanId] = useState<string | null>(null);

  const toggleSignInForm = () => setIsSignInOpen(prev => !prev);
  const toggleSignUpForm = () => setIsSignUpOpen(prev => !prev);

  return (
    <AuthFormsContext.Provider
      value={{
        isSignInOpen,
        isSignUpOpen,
        pendingPlanId,
        toggleSignInForm,
        toggleSignUpForm,
        setPendingPlanId,
      }}
    >
      {children}
    </AuthFormsContext.Provider>
  );
};

export const useAuthForms = () => {
  const context = useContext(AuthFormsContext);
  if (!context) {
    throw new Error('useAuthForms must be used within an AuthFormsProvider');
  }
  return context;
};
