import { useDispatch, useSelector } from 'react-redux';
import {
  useGetSubscriptionsPlansQuery,
  useSubscribeToPlanMutation,
  useGetUserSubscriptionPlanQuery,
} from '../../api/authApi';
import { BADGE_COLORS } from '../../constants/globalConstants';
import type { tSubscriptionPlan } from './types';
import type { AppState } from '../../store/store';
import { useAuthForms } from '../../context/AuthFormContext';
import { subscribe, unsubscribe } from '../../store/userSlice';
import { useState } from 'react';

export const useSubscriptionsPlans = () => {
  const dispatch = useDispatch();
  const { setPendingPlanId, toggleSignUpForm } = useAuthForms();
  const { id: userId, isLoggedIn } = useSelector((state: AppState) => state.user);

  const [alert, setAlert] = useState<{
    message: string;
    severity: 'success' | 'error';
  } | null>(null);

  const { data: plansData, isLoading, isError } = useGetSubscriptionsPlansQuery();
  const { data: userPlan, refetch: refetchUserPlan } = useGetUserSubscriptionPlanQuery(userId!, {
    skip: !userId,
  });

  const [subscribeToPlan] = useSubscribeToPlanMutation();

  const plans: tSubscriptionPlan[] =
    plansData?.map((plan, index) => ({
      id: plan.id,
      label: plan.sub_type,
      description: plan.sub_description,
      price: plan.sub_cost,
      badgeColor: BADGE_COLORS[index % BADGE_COLORS.length],
    })) ?? [];

  const handleSubscribe = async (plan: tSubscriptionPlan) => {
    if (!isLoggedIn) {
      setPendingPlanId(plan.id);
      toggleSignUpForm();
      return;
    }

    try {
      await subscribeToPlan({ user_id: userId || '', plan_id: plan.id }).unwrap();
      plan.label === 'Free' ? dispatch(unsubscribe()) : dispatch(subscribe());
      await refetchUserPlan();
      setAlert({
        message: `You have successfully subscribed to "${plan.label}" plan.`,
        severity: 'success',
      });
    } catch (err) {
      setAlert({
        message: 'Something went wrong. Please try again later.',
        severity: 'error',
      });
    }
  };

  return {
    plans,
    isLoading,
    isError,
    handleSubscribe,
    userPlan,
    alert,
    setAlert,
  };
};
