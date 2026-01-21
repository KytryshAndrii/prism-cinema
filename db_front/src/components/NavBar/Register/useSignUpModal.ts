import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerFormSchema } from '../../../schemas/authSchemas';
import { useRegisterUserMutation, useSubscribeToPlanMutation } from '../../../api/authApi';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { logIn, subscribe } from '../../../store/userSlice';
import { useState } from 'react';
import { useAuthForms } from '../../../context/AuthFormContext';
import { getRegionFromLocale } from '../../../utils/utils';
import type { tRegisterForm } from '../../../types/authTypes';

export const useSignUpModal = (onClose: () => void) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { pendingPlanId, setPendingPlanId } = useAuthForms();

  const [registerUser, { isLoading }] = useRegisterUserMutation();
  const [subscribeToPlan] = useSubscribeToPlanMutation();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<tRegisterForm>({
    resolver: zodResolver(registerFormSchema),
    mode: 'onTouched',
  });

  const onSubmit = async (formData: tRegisterForm) => {
    setErrorMessage(null);
    const region = getRegionFromLocale();
    try {
      const result = await registerUser({ ...formData, region }).unwrap();

      dispatch(
        logIn({
          id: result.id,
          login: result.login,
          email: result.email,
          token: result.token,
          birthday: formData.dateOfBirth,
          region: region,
          isLoggedIn: true,
          isUserSubscribed: false,
          isUserAdmin: false,
        })
      );

      if (pendingPlanId) {
        try {
          await subscribeToPlan({
            user_id: result.id,
            plan_id: pendingPlanId,
          }).unwrap();

          dispatch(subscribe());
          setPendingPlanId(null);
        } catch {
          console.error('Auto subscription failed');
        }
      }

      onClose();
      navigate('/films');
    } catch (error: any) {
      if (error?.status === 409) {
        setErrorMessage('User already exists. You can log in instead.');
        throw new Error('User already exists');
      } else if (error?.status === 400) {
        setErrorMessage('Invalid input data.');
        throw new Error('Invalid input data');
      } else if (error?.status === 500) {
        setErrorMessage('Server error. Please try again later.');
        throw new Error('Server error');
      } else {
        setErrorMessage('Unknown registration error.');
        throw new Error('Unknown registration error');
      }
    }
  };

  return {
    register,
    handleSubmit,
    onSubmit,
    errors,
    isLoading,
    errorMessage,
  };
};
