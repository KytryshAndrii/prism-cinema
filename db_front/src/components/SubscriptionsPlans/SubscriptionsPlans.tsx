import React from 'react';
import {
  Wrapper,
  PlansContainer,
  PlanCard,
  Badge,
  Description,
  Price,
  PriceCurrency,
  PriceValue,
  SubscribeButton,
} from './styles';
import { Box } from '@mui/material';
import type { AppState } from '../../store/store';
import { useSelector } from 'react-redux';
import { useAuthForms } from '../../context/AuthFormContext';

type SubscriptionPlan = {
  id: string;
  label: string;
  badgeColor: string;
  description: string;
  price: string;
};

const plans: SubscriptionPlan[] = [
  {
    id: 'free',
    label: 'FREE',
    badgeColor: '#455a64',
    description:
      'You have unlimited access to the full list of movies and their detailed information. However, you are not allowed to watch the movies.',
    price: '0.00',
  },
  {
    id: 'month',
    label: '1 MONTH',
    badgeColor: '#fb8c00',
    description:
      'Enjoy full access to all movies – you can stream them without any limitations and create your own lists of favorite titles. The subscription renews every month.',
    price: '97.17',
  },
  {
    id: 'six-month',
    label: '6 MONTH',
    badgeColor: '#1e88e5',
    description:
      'Includes all the features of the Monthly Plan. A one-time payment gives you access to the platform for 6 months – a convenient option for regular users.',
    price: '244.77',
  },
];

const SubscriptionPlans: React.FC = () => {

  const { isLoggedIn } = useSelector((state: AppState) => state.user);
  const { toggleSignUpForm } = useAuthForms();
  const handleSubscribe = (planId: string) => {
    if(!isLoggedIn){
      toggleSignUpForm();
      return;
    }
    console.log(planId)
    return; // HERE LOGIC OF PLAN CHANGE
    
  };

  return (
    <Wrapper>
      <PlansContainer>
        {plans.map((plan) => (
          <PlanCard key={plan.id}>
            <Box>
              <Badge color={plan.badgeColor}>{plan.label}</Badge>
              <Description>{plan.description}</Description>
            </Box>
            <Box>
              <Price>
                <PriceCurrency>PLN</PriceCurrency>
                <PriceValue>{plan.price}</PriceValue>
              </Price>
              <SubscribeButton onClick={() => handleSubscribe(plan.id)}>
                SUBSCRIBE
              </SubscribeButton> 
            </Box>
      
          </PlanCard>
        ))}
      </PlansContainer>
    </Wrapper>
  );
};

export default SubscriptionPlans;
