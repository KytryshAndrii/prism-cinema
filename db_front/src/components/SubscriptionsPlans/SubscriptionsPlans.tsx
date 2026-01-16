import React from "react";
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
  AlertWrapper,
  CurrentPlanText
} from "./styles";
import { Box, CircularProgress } from "@mui/material";
import { useSubscriptionsPlans } from "./useSubscriptionsPlans";

const SubscriptionPlans: React.FC = () => {
  const {
    plans,
    isLoading,
    handleSubscribe,
    userPlan,
    alert,
    setAlert,
  } = useSubscriptionsPlans();

  if (isLoading) return <CircularProgress />;

  return (
    <Wrapper>
      <PlansContainer>
        {plans.map((plan) => {
          const isCurrentPlan = plan.id === userPlan?.id;

          return (
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
                {isCurrentPlan ? (
                  <CurrentPlanText>Your Current Plan</CurrentPlanText>
                ) : (
                  <SubscribeButton onClick={() => handleSubscribe(plan)}>
                    SUBSCRIBE
                  </SubscribeButton>
                )}
              </Box>
            </PlanCard>
          );
        })}
      </PlansContainer>

      {alert && (
        <AlertWrapper
          severity={alert.severity}
          onClose={() => setAlert(null)}
        >
          {alert.message}
        </AlertWrapper>
      )}
    </Wrapper>
  );
};

export default SubscriptionPlans;
