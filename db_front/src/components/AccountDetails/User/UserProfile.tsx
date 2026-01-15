import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useSelector } from "react-redux";
import EditIcon from "@mui/icons-material/Edit";
import type { AppState } from "../../../store/store";
import { EditIconWrapper, FieldLabel, FieldRow, InfoBox, NonEditableUserData, ProfileTitle, ProfileWrapper, ReadOnlyText, SaveButton, StyledInput } from "./styles";
import type { tFormValues } from "./types";
import { useUserProfile } from "./useUserProfile";
import { Alert, CircularProgress } from "@mui/material";

const UserProfile: React.FC = () => {
  const user = useSelector((state: AppState) => state.user);

  const [isEditingLogin, setIsEditingLogin] = useState(false);
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [isEditingPassword, setIsEditingPassword] = useState(false);

  const {
    register,
    handleSubmit,
  } = useForm<tFormValues>({
    defaultValues: {
      login: user.login ?? "",
      email: user.email ?? "",
      password: "",
      confirmPassword: "",
    },
  });

  const {
    onSubmit,
    errorMsg,
    successMsg,
    isLoading,
  } = useUserProfile({
    isEditingLogin,
    isEditingEmail,
    isEditingPassword,
  });


  const cropDate = (date: string): string =>
    date ? new Date(date).toISOString().split("T")[0] : "";

  return (
    <ProfileWrapper onSubmit={handleSubmit(onSubmit)}>
      <ProfileTitle>PROFILE</ProfileTitle>

      <FieldLabel>Username</FieldLabel>
      <FieldRow>
        <StyledInput disabled={!isEditingLogin} {...register("login")} />
        <EditIconWrapper onClick={() => setIsEditingLogin(!isEditingLogin)}>
          <EditIcon />
        </EditIconWrapper>
      </FieldRow>

      <FieldLabel>Password</FieldLabel>
      <FieldRow>
        <StyledInput
          type="password"
          disabled={!isEditingPassword}
          {...register("password")}
        />
        <EditIconWrapper onClick={() => setIsEditingPassword(!isEditingPassword)}>
          <EditIcon />
        </EditIconWrapper>
      </FieldRow>

      {isEditingPassword && (
        <>
          <FieldLabel>Confirm Password</FieldLabel>
          <FieldRow>
            <StyledInput
              type="password"
              {...register("confirmPassword")}
            />
          </FieldRow>
        </>
      )}

      <FieldLabel>Email address</FieldLabel>
      <FieldRow>
        <StyledInput
          type="email"
          disabled={!isEditingEmail}
          {...register("email")}
        />
        <EditIconWrapper onClick={() => setIsEditingEmail(!isEditingEmail)}>
          <EditIcon />
        </EditIconWrapper>
      </FieldRow>

      <NonEditableUserData>
        <FieldLabel>Date of Birth:</FieldLabel>
        <ReadOnlyText>{cropDate(user.birthday!)}</ReadOnlyText>
      </NonEditableUserData>

      <NonEditableUserData>
        <FieldLabel>Region:</FieldLabel>
        <ReadOnlyText>{user.region}</ReadOnlyText>
      </NonEditableUserData>
      <InfoBox>
        {errorMsg && <Alert severity="warning">{errorMsg}</Alert>}
        {successMsg && <Alert severity="success">{successMsg}</Alert>}
      </InfoBox>
      <SaveButton type="submit" disabled={isLoading}>
        {isLoading ? <CircularProgress size={20} /> : "Save changes"}
      </SaveButton>
    </ProfileWrapper>
  );
};

export default UserProfile;
