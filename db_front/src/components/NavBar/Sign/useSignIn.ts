import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginRequestSchema } from "../../../schemas/authSchemas";
import type { tLoginRequest } from "../../../types/authTypes";
import { useLoginUserMutation } from "../../../api/authApi";
import { useDispatch } from "react-redux";
import { logIn } from "../../../store/userSlice";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export const useSignIn = (onClose: () => void) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [loginUser, { isLoading }] = useLoginUserMutation();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<tLoginRequest>({
    resolver: zodResolver(loginRequestSchema),
    mode: "onTouched",
  });

  const onSubmit = async (formData: tLoginRequest) => {
    setErrorMessage(null);

    try {
      const result = await loginUser(formData).unwrap();

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
      if (error?.status === 401) {
        setErrorMessage("Incorrect login or password.");
        throw new Error("Incorrect login or password.");
      } else if (error?.status === 500) {
        setErrorMessage("Server error. Please try again later.");
        throw new Error("Server error. Please try again later.");
    } else {
        setErrorMessage("Login failed.");
        throw new Error("Login failed. Unknowned error.");
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
