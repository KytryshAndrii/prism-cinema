import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerRequestSchema } from "../../../schemas/authSchemas";
import { useRegisterUserMutation } from "../../../api/authApi";
import type { tRegisterForm } from "./types";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { logIn } from "../../../store/userSlice";
import { useState } from "react";

export const useSignUpModal = (onClose: () => void) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [registerUser, { isLoading }] = useRegisterUserMutation();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<tRegisterForm>({
    resolver: zodResolver(registerRequestSchema),
    mode: "onTouched",
  });

   const onSubmit = async (formData: tRegisterForm) => {
    setErrorMessage(null); 
    try {
      const result = await registerUser(formData).unwrap();

      dispatch(
        logIn({
          id: result.id,
          login: result.login,
          email: result.email,
          token: result.token,
          isLoggedIn: true,
        })
      );

      onClose();
      navigate("/films");
    } catch (error: any) {
       if (error?.status === 409) {
        setErrorMessage("User already exists. You can log in instead.");
        throw new Error("User already exists");
      } else if (error?.status === 400) {
        setErrorMessage("Invalid input data.");
        throw new Error("Invalid input data");
      } else if (error?.status === 500) {
        setErrorMessage("Server error. Please try again later.");
        throw new Error("Server error");
      } else {
        setErrorMessage("Unknown registration error.");
        throw new Error("Unknown registration error");
      }
    }
  };

  return {
    register,
    handleSubmit,
    onSubmit,
    errors,
    isLoading,
    errorMessage
  };
};
