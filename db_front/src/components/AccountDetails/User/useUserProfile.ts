import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { AppState } from "../../../store/store";
import { useUpdateUserProfileMutation } from "../../../api/authApi";
import { updateUser } from "../../../store/userSlice";
import type { tFormValues } from "./types";

export const useUserProfile = ({
  isEditingLogin,
  isEditingEmail,
  isEditingPassword,
}: {
  isEditingLogin: boolean;
  isEditingEmail: boolean;
  isEditingPassword: boolean;
}) => {
  const user = useSelector((state: AppState) => state.user);
  const dispatch = useDispatch();

  const [updateUserProfile, { isLoading }] =
    useUpdateUserProfileMutation();

  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const onSubmit = async (data: tFormValues) => {
    setErrorMsg(null);
    setSuccessMsg(null);

    const loginChanged = isEditingLogin && data.login !== user.login;
    const emailChanged = isEditingEmail && data.email !== user.email;

    if (isEditingPassword) {
      if (!data.password || !data.confirmPassword) {
        setErrorMsg("Password fields cannot be empty.");
        return;
      }
      if (data.password !== data.confirmPassword) {
        setErrorMsg("Passwords do not match.");
        return;
      }
    }

    if (!loginChanged && !emailChanged && !isEditingPassword) {
      setErrorMsg("No changes detected.");
      return;
    }

    try {
      await updateUserProfile({
        userId: user.id!,
        login: loginChanged ? data.login : undefined,
        email: emailChanged ? data.email : undefined,
        password: isEditingPassword ? data.password : undefined,
      }).unwrap();

      dispatch(
        updateUser({
          login: loginChanged ? data.login : user.login!,
          email: emailChanged ? data.email : user.email!,
        })
      );

      setSuccessMsg("Profile updated successfully !");
    } catch (error: any) {
      const status = error?.status;

      if (status === 400) {
        setErrorMsg("Invalid data. Please check fields.");
        throw new Error("Invalid data. Please check fields.");
      } else if (status === 401) {
        setErrorMsg("Session expired. Please log in again.");
        throw new Error("Session expired. Please log in again.");
      } else if (status === 409) {
        setErrorMsg("Login or email already exists.");
        throw new Error("Login or email already exists.");
      } else {
        setErrorMsg("Server error. Try again later.");
        throw new Error("Server error. Try again later.");
      }
    }
  };

  return {
    onSubmit,
    errorMsg,
    successMsg,
    isLoading,
  };
};
